from m2c2_datakit.tasks import color_dots, grid_memory, symbol_search, shopping_list, symbol_number_matching

DEFAULT_FUNC_MAP_SCORING = {
    "Grid Memory": [
        ("error_distance_hausdorff", grid_memory.score_hausdorff),
        ("error_distance_mean", grid_memory.score_mean_error),
        ("error_distance_sum", grid_memory.score_sum_error),
    ],
    "Symbol Search": [
        ("accuracy", symbol_search.score_accuracy),
    ],
}