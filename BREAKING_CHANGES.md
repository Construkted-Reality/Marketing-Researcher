# Breaking Changes: Pain Points → Insights Refactor

## Overview
The `spt_researcher.py` script has been refactored to replace all "pain point" terminology with "insights" to broaden the script's purpose beyond just identifying user problems.

## Breaking Changes

### 1. CLI Flag Changes
- **REMOVED**: `--pain-points-output` 
- **ADDED**: `--insights-output` (default: `insights.md`)
- **REMOVED**: `--max-points`
- **ADDED**: `--max-insights`

### 2. Default Output File Changes
- **Old default**: `pain_points.md`
- **New default**: `insights.md`

### 3. Function Name Changes
- **`get_pain_points()`** → **`get_insights()`**
- Function signature changed from `get_pain_points(topic: str, max_points: int, ...)` to `get_insights(topic: str, max_insights: int, ...)`

### 4. Variable Name Changes
- `pain_points` → `insights`
- `pain_point` → `insight`
- `max_points` → `max_insights`

### 5. Prompt and Output Changes
- Prompts now request "actionable insights and key topics" instead of "pain points"
- Debug output headers changed from "Pain Points Debug Session" to "Insights Debug Session"
- Debug sections changed from "Parsed Pain Points" to "Parsed Insights"

## Migration Guide

### For CLI Users
**Before:**
```bash
python spt_researcher.py --topic "remote work" --max-points 10 --pain-points-output "my_points.md"
```

**After:**
```bash
python spt_researcher.py --topic "remote work" --max-insights 10 --insights-output "my_insights.md"
```

### For API Users
**Before:**
```python
insights, prompt, raw = await get_pain_points(topic, max_points=15)
```

**After:**
```python
insights, prompt, raw = await get_insights(topic, max_insights=15)
```

### For Test Suite
- Update test files to use `--max-insights` instead of `--max-points`
- Existing `pain_points.md` files will no longer be created by default

## Files Modified
- `spt_researcher.py` - Complete refactor of terminology
- `SPT_RESEARCHER_GUIDE.md` - Updated documentation and examples
- `test_spt_researcher.py` - Updated CLI flags in tests
- `.kilocode/rules/memory-bank/context.md` - Updated feature descriptions
- `.kilocode/rules/memory-bank/tasks.md` - Updated task documentation

## Backward Compatibility
**No backward compatibility is maintained.** The old CLI flags and function names are completely removed. Users must update their scripts and workflows to use the new terminology.

---
*Generated on September 8, 2025 as part of the insights terminology refactor*