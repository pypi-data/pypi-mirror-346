from __future__ import annotations

import logging
from collections.abc import Callable, Mapping
from functools import partial
from typing import Any

import polars as pl

from functime.metrics import mae

try:
    import flaml
    from flaml import CFO
    from flaml.tune.sample import Domain
except ImportError:
    pass


def evaluate_window(
    config: Mapping[str, Any],
    lags: int,
    test_size: int,
    max_horizons: int,
    strategy: str,
    freq: str,
    forecaster_cls: Callable,
    y_train: pl.DataFrame,
    y_test: pl.DataFrame,
    X_train: pl.DataFrame | None = None,
    X_test: pl.DataFrame | None = None,
) -> float | pl.DataFrame:
    # Train test split
    entity_col, time_col = y_train.columns[:2]
    # Fit
    config = config or {}
    forecaster = forecaster_cls(
        lags=lags, freq=freq, max_horizons=max_horizons, strategy=strategy, **config
    )
    try:
        forecaster.fit(y=y_train, X=X_train)
        y_pred = forecaster.predict(fh=test_size, X=X_test)
        # NOTE: Defensive match of entity, time indices
        # Need to do this for example if the train set is "1i", but the
        # test set starts from 1,2,3,...,fh
        # Assumes y_test and y_pred align up
        y_test = y_test.sort([entity_col, time_col])
        y_pred = y_pred.sort([entity_col, time_col]).with_columns(
            y_test.get_column(time_col)
        )
        score = mae(y_true=y_test, y_pred=y_pred).get_column("mae").mean()
        res = {"score": score}
    except ValueError as exc:
        # AttributeError: 'NoneType' object has no attribute 'last_result'
        # Root cause: y_preds are inf hence mae = inf
        logging.warning(
            "%s fit-predict failed with lags %s and parameters %s",
            forecaster_cls.func,
            lags,
            config,
            exc_info=exc,
        )
        res = None
    return res


def evaluate_windows(
    config,
    lags: int,
    n_splits: int,
    test_size: int,
    max_horizons: int,
    strategy: str,
    freq: str,
    forecaster_cls: Callable,
    y_splits: Mapping[int, tuple[pl.DataFrame, pl.DataFrame]],
    X_splits: Mapping[int, tuple[pl.DataFrame, pl.DataFrame]] | None,
):
    # Get average mae across splits
    results = []
    for i in range(n_splits):
        y_train, y_test = y_splits[i]
        X_train = None
        X_test = None
        if X_splits is not None:
            X_train, X_test = X_splits[i]
        result = evaluate_window(
            y_train=y_train,
            y_test=y_test,
            X_train=X_train,
            X_test=X_test,
            config=config,
            lags=lags,
            test_size=test_size,
            max_horizons=max_horizons,
            strategy=strategy,
            freq=freq,
            forecaster_cls=forecaster_cls,
        )
        results.append(result)
    scores = [res["score"] for res in results]
    score = None
    if len(scores) > 0:
        score = sum(scores) / len(scores)
    else:
        raise ValueError("Failed to evaluate every window")
    res = {"mae": score}
    return res


def evaluate(
    lags: int,
    n_splits: int,
    time_budget: int,
    points_to_evaluate: list[Mapping[str, Any]],
    num_samples: int,
    low_cost_partial_config: Mapping[str, Any],
    test_size: int,
    max_horizons: int,
    strategy: str,
    freq: str,
    forecaster_cls: Callable,
    y_splits: Mapping[int, tuple[pl.DataFrame, pl.DataFrame]],
    X_splits: Mapping[int, tuple[pl.DataFrame, pl.DataFrame]] | None,
    search_space: Mapping[str, Domain] | None = None,
    include_best_params: bool = False,
):
    params = None
    if search_space is None:
        result = evaluate_windows(
            config=params,
            lags=lags,
            n_splits=n_splits,
            test_size=test_size,
            max_horizons=max_horizons,
            strategy=strategy,
            freq=freq,
            forecaster_cls=forecaster_cls,
            y_splits=y_splits,
            X_splits=X_splits,
        )
        score = result["mae"]
    else:
        tuner = flaml.tune.run(
            partial(
                evaluate_windows,
                lags=lags,
                n_splits=n_splits,
                test_size=test_size,
                max_horizons=max_horizons,
                strategy=strategy,
                freq=freq,
                forecaster_cls=forecaster_cls,
                y_splits=y_splits,
                X_splits=X_splits,
            ),
            config=search_space,
            metric="mae",
            mode="min",
            time_budget_s=time_budget,
            points_to_evaluate=points_to_evaluate,
            num_samples=num_samples,
            search_alg=CFO(low_cost_partial_config=low_cost_partial_config),
        )
        score = tuner.best_result["mae"]
        params = tuner.best_config

    if include_best_params:
        return score, params
    else:
        return score
