You are a content marketing analyst. Extract {max_insights} specific, actionable insights from the research below for the topic "{topic}".

For each insight, provide:
- A concise, actionable insight statement (insight)
- Key context or supporting details (context)
- Relevant source references (source_reference)
- Key metrics or data points (key_data)
- Priority level for content creation (priority_level)
- Suggested content type (content_type)
- Target audience (target_audience)

Return ONLY a valid JSON array of objects with the following structure:
[
  {
    "insight": "string",
    "context": "string",
    "source_reference": "string",
    "key_data": "string",
    "priority_level": "string",
    "content_type": "string",
    "target_audience": "string"
  },
  ...
]

Example:
[
  {
    "insight": "Inconsistent lighting causes photogrammetry errors",
    "context": "Poor lighting leads to mismatched features in images, resulting in alignment failures",
    "source_reference": "https://example.com/lighting-issues",
    "key_data": "80% of failed projects cite lighting as the top issue",
    "priority_level": "high",
    "content_type": "troubleshooting",
    "target_audience": "technical"
  },
  {
    "insight": "Overlapping images improve 3D reconstruction accuracy",
    "context": "Aim for 70-80% overlap between adjacent photos to ensure sufficient feature matching",
    "source_reference": "https://example.com/overlap-rules",
    "key_data": "15% reduction in errors with 75% overlap vs 50% overlap",
    "priority_level": "medium",
    "content_type": "how-to",
    "target_audience": "general"
  }
]

Research to analyze:
{truncated_raw}