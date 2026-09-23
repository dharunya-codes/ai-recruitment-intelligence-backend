from app.services.analysis_cache_service import AnalysisCache, make_analysis_cache_key


def test_identical_analysis_inputs_are_reused() -> None:
    cache = AnalysisCache(max_entries=4)
    calls = {"count": 0}

    def compute() -> dict[str, int]:
        calls["count"] += 1
        return {"value": calls["count"]}

    key = make_analysis_cache_key(
        owner_scope=10,
        resume_text="Python project",
        job_context={"requirements": ["Python"]},
        target_role="Backend Developer",
    )
    assert cache.get_or_compute(key, compute) == {"value": 1}
    assert cache.get_or_compute(key, compute) == {"value": 1}
    assert calls["count"] == 1
    assert cache.stats() == {"entries": 1, "hits": 1, "misses": 1}


def test_cache_key_changes_for_owner_role_job_and_resume_inputs() -> None:
    base = {
        "owner_scope": 1,
        "resume_text": "Python project",
        "job_context": {"job_id": 5, "description": "Python required"},
        "target_role": "Backend Developer",
    }
    base_key = make_analysis_cache_key(**base)
    assert make_analysis_cache_key(**{**base, "owner_scope": 2}) != base_key
    assert make_analysis_cache_key(**{**base, "target_role": "Data Analyst"}) != base_key
    assert make_analysis_cache_key(**{**base, "resume_text": "Docker project"}) != base_key
    assert make_analysis_cache_key(**{**base, "job_context": {"job_id": 6, "description": "Docker required"}}) != base_key


def test_changed_input_recomputes_and_cache_is_bounded() -> None:
    cache = AnalysisCache(max_entries=2)
    calls = {"count": 0}

    def compute() -> int:
        calls["count"] += 1
        return calls["count"]

    keys = [
        make_analysis_cache_key(owner_scope=1, resume_text=str(index), job_context={}, target_role="Role")
        for index in range(3)
    ]
    assert cache.get_or_compute(keys[0], compute) == 1
    assert cache.get_or_compute(keys[1], compute) == 2
    assert cache.get_or_compute(keys[2], compute) == 3
    assert cache.stats()["entries"] == 2
    assert cache.get_or_compute(keys[0], compute) == 4


def test_cache_values_are_isolated_from_callers() -> None:
    cache = AnalysisCache()
    key = make_analysis_cache_key(owner_scope=1, resume_text="resume", job_context={}, target_role="Role")
    first = cache.get_or_compute(key, lambda: {"items": ["Python"]})
    first["items"].append("Docker")
    second = cache.get_or_compute(key, lambda: {"items": ["wrong"]})
    assert second == {"items": ["Python"]}