#pragma once

#include <dset.h>

#include <nanoflann.hpp>

#include "types.hpp"

#include <taskflow/algorithm/for_each.hpp>
#include <taskflow/taskflow.hpp>

namespace nb = nanobind;

namespace dendroptimized
{

template <typename real_t>
static VecIndex<int32_t> connected_components(RefCloud<real_t> xyz, const real_t eps, const uint32_t min_samples)
{
    using kd_tree_t = nanoflann::KDTreeEigenMatrixAdaptor<RefCloud<real_t>, 3, nanoflann::metric_L2_Simple>;

    // Parallel construction of kdtree index is enabled by default, but maybe we have to adapt this
    // for small point clouds
    kd_tree_t    kd_tree(3, xyz, 10, 0);
    const real_t sq_search_radius = eps * eps;

    const Eigen::Index n_points = xyz.rows();

    tf::Executor                           executor;
    tf::Taskflow                           taskflow;
    std::vector<std::vector<Eigen::Index>> nn_cells(n_points);
    std::vector<bool>                      is_core(n_points, false);
    VecIndex<int32_t>                      cluster_id(n_points);
    cluster_id.fill(-1);

    taskflow.for_each_index(
        Eigen::Index(0), n_points, Eigen::Index(1),
        [&](Eigen::Index point_id)
        {
            std::vector<nanoflann::ResultItem<Eigen::Index, real_t>> result_set;

            nanoflann::RadiusResultSet<real_t, Eigen::Index> radius_result_set(sq_search_radius, result_set);
            const auto                                       num_found =
                kd_tree.index_->radiusSearchCustomCallback(xyz.row(point_id).data(), radius_result_set);

            if (num_found > 28)
            {
                // TODO: throw as it's too much, we only expect 27 NN + the base point
                throw std::invalid_argument(
                    "it seems that your radius is too big, CC extraction is only meant to be used in "
                    "27-connectivity "
                    "context on regular voxels grids");
            }

            is_core[point_id] = num_found >= min_samples;  // we include the core sample itself
            std::vector<Eigen::Index> nn_ids;
            nn_ids.reserve(num_found - 1);
            for (const auto& result : result_set)
            {
                if (result.first != point_id) { nn_ids.push_back(result.first); }
            }

            nn_cells[point_id] = std::move(nn_ids);
        },
        tf::StaticPartitioner(0));
    executor.run(taskflow).get();

    // Link core with disjoint set
    // no parallel since it does not seems to lower the runtime
    DisjointSets uf(n_points);
    for (size_t curr_id = 0; curr_id < n_points; ++curr_id)
    {
        if (!is_core[curr_id]) continue;
        for (const auto nn_id : nn_cells[curr_id])
        {
            if (is_core[nn_id] && curr_id > nn_id && uf.find(curr_id) != uf.find(nn_id)) { uf.unite(curr_id, nn_id); }
        }
    };

    // label core points in //
    auto label_core = taskflow.for_each_index(
        size_t(0), size_t(n_points), size_t(1),
        [&](size_t curr_id)
        {
            if (!is_core[curr_id]) return;
            cluster_id[curr_id] = uf.find(curr_id);
        });

    // label other nodes as borders in //
    // borders are attributed to their nearest cluster
    auto label_border = taskflow.for_each_index(
        size_t(0), size_t(n_points), size_t(1),
        [&](size_t curr_id)
        {
            if (!is_core[curr_id])
            {
                real_t min_dist = std::numeric_limits<real_t>::max();
                for (const auto nn_id : nn_cells[curr_id])
                {
                    if (is_core[nn_id])
                    {
                        real_t dist = (xyz.row(nn_id) - xyz.row(curr_id)).squaredNorm();
                        if (dist < min_dist)
                        {
                            min_dist            = dist;
                            cluster_id[curr_id] = cluster_id[nn_id];
                        }
                    }
                }
            }
        });

    label_border.succeed(label_core);

    executor.run(taskflow).get();

    return cluster_id;
}
}  // namespace dendroptimized
