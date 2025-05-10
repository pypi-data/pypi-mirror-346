#pragma once

#include <nanobind/eigen/dense.h>
#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <nanobind/stl/tuple.h>
#include <nanobind/stl/variant.h>

#include <Eigen/Dense>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <taskflow/algorithm/for_each.hpp>
#include <taskflow/algorithm/scan.hpp>
#include <taskflow/algorithm/sort.hpp>
#include <taskflow/algorithm/transform.hpp>

#include "types.hpp"
namespace nb = nanobind;

namespace dendroptimized
{

// low level version with Taskflow
template <typename real_t>
static std::tuple<PointCloud<real_t>, VecIndex<uint32_t>, VecIndex<uint32_t>> voxelize(
    DRefMatrixCloud<real_t> xyz, const real_t res_xy, const real_t res_z, const uint32_t id_x, const uint32_t id_y,
    const uint32_t id_z, const bool verbose)
{
    // number of bit used to encode one dimension
    constexpr uint64_t voxel_bits     = 21;
    constexpr uint64_t two_voxel_bits = 42;
    constexpr uint64_t num_cells      = 2097151;  // 2^21 -1 TODO: make this an exception if we need more

    // The coordinate minima
    const auto start_total = std::chrono::high_resolution_clock::now();

    if (verbose) nb::print(nb::str("-Voxelization\n Voxel resolution: {} x {} x {} m").format(res_xy, res_xy, res_z));

    tf::Executor executor;
    tf::Taskflow tf;

    const Eigen::Index num_points = xyz.rows();

    // Lambda to compute min in one dimension
    const auto min_one_dim = [&xyz, num_points](const Eigen::Index id_dim, real_t& min_dim)
    {
        min_dim = xyz(0, id_dim);
        for (Eigen::Index point_id = 1; point_id < num_points; ++point_id)
        {
            if (xyz(point_id, id_dim) < min_dim) min_dim = xyz(point_id, id_dim);
        };
    };

    // Parallel min coeff
    real_t min_x, min_y, min_z;
    tf.emplace([&]() { min_one_dim(id_x, min_x); });
    tf.emplace([&]() { min_one_dim(id_y, min_y); });
    tf.emplace([&]() { min_one_dim(id_z, min_z); });
    executor.run(tf).wait();

    const Vec3<real_t> min_vec(min_x, min_y, min_z);

    // Lambda to compute voxel hashing
    const auto create_hash = [&](const Eigen::RowVector<real_t, -1>& point) -> uint64_t
    {
        return ((static_cast<uint64_t>(std::floor((point(id_z) - min_vec(2)) / res_z)) << two_voxel_bits) |
                (static_cast<uint64_t>(std::floor((point(id_y) - min_vec(1)) / res_xy)) << voxel_bits)) |
               static_cast<uint64_t>(std::floor((point(id_x) - min_vec(0)) / res_xy));
    };

    std::vector<uint64_t> hashes(num_points);
    VecIndex<uint32_t>    cloud_to_vox_ind(num_points);
    PointCloud<real_t>    vox_pc;
    VecIndex<uint32_t>    vox_to_cloud_ind;

    std::vector<uint32_t> first_point_in_vox(num_points, 0);
    first_point_in_vox[0] = 1;

    std::vector<Eigen::Index>           sorted_indices(num_points);
    std::vector<Eigen::Index>::iterator first_it_indices = sorted_indices.begin();
    std::vector<Eigen::Index>::iterator end_it_indices   = sorted_indices.end();
    std::iota(first_it_indices, end_it_indices, 0);

    // Timing variables and tasks
    std::chrono::time_point<std::chrono::high_resolution_clock> start_hashing, stop_hashing, start_sorting,
        stop_sorting, start_grouping, stop_grouping, start_voxelization, stop_voxelization;

    auto start_hashing_task =
        tf.emplace([&start_hashing]() { start_hashing = std::chrono::high_resolution_clock::now(); });
    auto stop_hashing_task =
        tf.emplace([&stop_hashing]() { stop_hashing = std::chrono::high_resolution_clock::now(); });

    auto start_sorting_task =
        tf.emplace([&start_sorting]() { start_sorting = std::chrono::high_resolution_clock::now(); });
    auto stop_sorting_task =
        tf.emplace([&stop_sorting]() { stop_sorting = std::chrono::high_resolution_clock::now(); });

    auto start_grouping_task =
        tf.emplace([&start_grouping]() { start_grouping = std::chrono::high_resolution_clock::now(); });
    auto stop_grouping_task =
        tf.emplace([&stop_grouping]() { stop_grouping = std::chrono::high_resolution_clock::now(); });

    auto start_voxelization_task =
        tf.emplace([&start_voxelization]() { start_voxelization = std::chrono::high_resolution_clock::now(); });
    auto stop_voxelization_task =
        tf.emplace([&stop_voxelization]() { stop_voxelization = std::chrono::high_resolution_clock::now(); });

    // Create hashes
    auto hashing = tf.for_each(
                         std::cref(first_it_indices), std::cref(end_it_indices),
                         [&](const Eigen::Index point_id) { hashes[point_id] = create_hash(xyz.row(point_id)); })
                       .name("hashing");

    // second order point by dimensions
    auto sort_indices = tf.sort(
                              std::cref(first_it_indices), std::cref(end_it_indices),
                              [&](const Eigen::Index a, Eigen::Index b) { return hashes[a] < hashes[b]; })
                            .name("sort_indices");  // note this is not a stable sort

    // In the sorted index find first representent one voxel cell
    auto unique = tf.for_each_index(
                        Eigen::Index(1), Eigen::Index(num_points), Eigen::Index(1),
                        [&](const Eigen::Index point_id)
                        {
                            if (hashes[sorted_indices[point_id]] != hashes[sorted_indices[point_id - 1]])
                            {
                                first_point_in_vox[point_id] = 1;
                            }
                        })
                      .name("unique");

    // count and generate voxel id with a parallel scan
    auto count_voxels =
        tf.inclusive_scan(
              first_point_in_vox.begin(), first_point_in_vox.end(), first_point_in_vox.begin(), std::plus<int>{})
            .name("count_voxels");

    // allocate voxel point cloud and vox_to_cloud
    auto allocate = tf.emplace(
        [&]()
        {
            vox_pc           = PointCloud<real_t>(first_point_in_vox.back(), 3);
            vox_to_cloud_ind = VecIndex<uint32_t>(first_point_in_vox.back());
        });

    // Precomputed shifts for each dimensional composant of a full hashed code
    const real_t centroid_shift_x = min_vec(0) + res_xy / real_t(2.0);
    const real_t centroid_shift_y = min_vec(1) + res_xy / real_t(2.0);
    const real_t centroid_shift_z = min_vec(2) + res_z / real_t(2.0);

    auto fill_vox_pc = tf.for_each_index(
                             Eigen::Index(0), Eigen::Index(num_points), Eigen::Index(1),
                             [&](const Eigen::Index point_id)
                             {
                                 const auto voxel_id             = first_point_in_vox[point_id] - 1;  // it starts at 1
                                 const auto real_point_id        = sorted_indices[point_id];
                                 cloud_to_vox_ind(real_point_id) = voxel_id;
                                 //  we account for the first point here
                                 //  maybe it could be better to init. it in the allocation tasks
                                 if (point_id == 0 || voxel_id != first_point_in_vox[point_id - 1] - 1)
                                 {
                                     vox_to_cloud_ind(voxel_id) = real_point_id;
                                     const uint64_t hash_val    = hashes[real_point_id];

                                     const uint64_t z_code_val = hash_val >> two_voxel_bits;
                                     const uint64_t y_code_val = (hash_val >> voxel_bits) & num_cells;
                                     const uint64_t x_code_val = hash_val & num_cells;

                                     vox_pc(voxel_id, 0) = x_code_val * res_xy + centroid_shift_x;
                                     vox_pc(voxel_id, 1) = y_code_val * res_xy + centroid_shift_y;
                                     vox_pc(voxel_id, 2) = z_code_val * res_z + centroid_shift_z;
                                 }
                             })
                           .name("fill_vox_pc");

    // Taskflow workflow
    // Group timings task here
    start_hashing_task.precede(hashing);
    stop_hashing_task.succeed(hashing);
    start_sorting_task.precede(sort_indices);
    stop_sorting_task.succeed(sort_indices);
    start_grouping_task.precede(unique);
    stop_grouping_task.succeed(count_voxels);
    start_voxelization_task.precede(allocate);
    stop_voxelization_task.succeed(fill_vox_pc);

    // Group tasks here
    hashing.precede(sort_indices);
    sort_indices.precede(unique);
    unique.precede(count_voxels);
    count_voxels.precede(allocate);
    allocate.precede(fill_vox_pc);

    // Launch tasks
    executor.run(tf).wait();

    std::stringstream log;

    log << "  Hashing in "
        << std::chrono::duration_cast<std::chrono::milliseconds>(stop_hashing - start_hashing).count() << " ms\n"
        << "  Sorting in "
        << std::chrono::duration_cast<std::chrono::milliseconds>(stop_sorting - start_sorting).count() << " ms\n"
        << "  Grouping in "
        << std::chrono::duration_cast<std::chrono::milliseconds>(stop_grouping - start_grouping).count() << " ms\n"
        << "  Voxelization in "
        << std::chrono::duration_cast<std::chrono::milliseconds>(stop_voxelization - start_voxelization).count()
        << " ms\n"
        << "  Total time "
        << std::chrono::duration_cast<std::chrono::milliseconds>(
               std::chrono::high_resolution_clock::now() - start_total)
               .count()
        << " ms\n"
        << std::setprecision(3) << std::fixed << "  " << num_points / 1.0e6 << " million points -> "
        << vox_pc.rows() / 1.0e6 << " millions voxels\n"
        << "  Voxels account for " << vox_pc.rows() * 100 / static_cast<double>(num_points) << "% of original points";

    if (verbose) nb::print(log.str().c_str());

    return {vox_pc, cloud_to_vox_ind, vox_to_cloud_ind};
}

template <typename real_t>
static std::variant<
    std::tuple<PointCloud<real_t>, VecIndex<uint32_t>, VecIndex<uint32_t>>,
    std::tuple<PointCloudAugmented<real_t>, VecIndex<uint32_t>, VecIndex<uint32_t>>>
    voxelize_wrapper(
        DRefMatrixCloud<real_t> xyz, const real_t res_xy, const real_t res_z, const uint32_t n_digits, uint32_t id_x,
        const uint32_t id_y, const uint32_t id_z, const bool with_n_points, const bool verbose)
{
    if (with_n_points)
    {
        auto                        res               = voxelize(xyz, res_xy, res_z, id_x, id_y, id_z, verbose);
        PointCloudAugmented<real_t> vox_cloud_num_pts = PointCloudAugmented<real_t>::Zero(std::get<2>(res).size(), 4);

        const auto& vox_cloud         = std::get<0>(res);
        vox_cloud_num_pts.leftCols(3) = vox_cloud;
        const auto& cloud_to_vox_id   = std::get<1>(res);
        for (const auto vox_id : cloud_to_vox_id) { vox_cloud_num_pts(vox_id, 3)++; }

        return std::make_tuple(vox_cloud_num_pts, cloud_to_vox_id, std::get<2>(res));
    }
    else { return voxelize(xyz, res_xy, res_z, id_x, id_y, id_z, verbose); }
}

}  // namespace dendroptimized
