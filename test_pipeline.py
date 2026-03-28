"""
Tests for Phase 1 pipeline additions:
  - strip_html()
  - tag_diff()
  - build_timeline() field coverage (behavioral_tags, content_raw,
    content_snapshot, prompt_length)

Previous injection-scoring tests have been removed along with the feature.
See archive/SPEC_scoring.md for removal rationale.
"""

import unittest
from extract_and_analyze import strip_html, tag_diff, build_timeline


class TestStripHtml(unittest.TestCase):

    def test_strips_tags(self):
        self.assertEqual(strip_html("<p>Hello</p>"), "Hello")

    def test_strips_nested_tags(self):
        self.assertEqual(strip_html("<div><span>text</span></div>"), "text")

    def test_collapses_whitespace(self):
        result = strip_html("<p>one</p>   <p>two</p>")
        self.assertEqual(result, "one two")

    def test_plain_text_unchanged(self):
        self.assertEqual(strip_html("no tags here"), "no tags here")

    def test_empty_string(self):
        self.assertEqual(strip_html(""), "")

    def test_strips_attributes(self):
        result = strip_html('<div class="pref-card" id="x">content</div>')
        self.assertEqual(result, "content")


class TestTagDiff(unittest.TestCase):

    def _make_diff(self, added=None, removed=None):
        return {"added": added or [], "removed": removed or []}

    def test_safety_tag_on_refuse(self):
        diff = self._make_diff(added=["you must refuse harmful requests"])
        self.assertIn("safety", tag_diff(diff))

    def test_tool_definition_tag(self):
        diff = self._make_diff(added=['"name": "get_weather", "parameters": {}'])
        self.assertIn("tool_definition", tag_diff(diff))

    def test_persona_tag(self):
        diff = self._make_diff(added=["you are a helpful assistant with a friendly tone"])
        self.assertIn("persona", tag_diff(diff))

    def test_capability_tag(self):
        diff = self._make_diff(added=["users are now able to upload files"])
        self.assertIn("capability", tag_diff(diff))

    def test_formatting_tag(self):
        diff = self._make_diff(added=["use markdown for all responses"])
        self.assertIn("formatting", tag_diff(diff))

    def test_memory_tag(self):
        diff = self._make_diff(added=["remember user preferences across the conversation"])
        self.assertIn("memory", tag_diff(diff))

    def test_policy_tag(self):
        diff = self._make_diff(added=["comply with all applicable privacy laws"])
        self.assertIn("policy", tag_diff(diff))

    def test_other_when_no_match(self):
        diff = self._make_diff(added=["the sky is blue"])
        self.assertEqual(tag_diff(diff), ["other"])

    def test_multiple_tags(self):
        diff = self._make_diff(added=["refuse harmful requests and follow policy guidelines"])
        tags = tag_diff(diff)
        self.assertIn("safety", tags)
        self.assertIn("policy", tags)

    def test_case_insensitive(self):
        diff = self._make_diff(added=["You Must Refuse all HARMFUL requests"])
        self.assertIn("safety", tag_diff(diff))

    def test_removed_lines_also_checked(self):
        diff = self._make_diff(removed=["refuse to answer questions about weapons"])
        self.assertIn("safety", tag_diff(diff))


class TestBuildTimelineFields(unittest.TestCase):
    """Verify new Phase 1 fields are present on every timeline entry."""

    def _make_versions(self, content_old, content_new):
        return [
            {
                "hash": "aaaaaaaa",
                "full_hash": "aaaaaaaabbbbbbbbccccccccdddddddd",
                "date": "2026-02-01T00:00:00+00:00",
                "message": "update prompt",
                "content": content_new,
                "filepath": "Anthropic/claude.html",
            },
            {
                "hash": "bbbbbbbb",
                "full_hash": "bbbbbbbbccccccccddddddddeeeeeeee",
                "date": "2026-01-01T00:00:00+00:00",
                "message": "initial prompt",
                "content": content_old,
                "filepath": "Anthropic/claude.html",
            },
        ]

    def test_behavioral_tags_present(self):
        versions = self._make_versions("hello world", "refuse harmful requests")
        timeline = build_timeline(versions)
        self.assertTrue(len(timeline) > 0)
        self.assertIn("behavioral_tags", timeline[0])

    def test_content_raw_is_raw_content(self):
        versions = self._make_versions("old", "<p>new content</p>")
        timeline = build_timeline(versions)
        self.assertEqual(timeline[0]["content_raw"], "<p>new content</p>")

    def test_content_snapshot_is_stripped(self):
        versions = self._make_versions("old", "<p>new content</p>")
        timeline = build_timeline(versions)
        self.assertEqual(timeline[0]["content_snapshot"], "new content")

    def test_prompt_length_matches_snapshot(self):
        versions = self._make_versions("old", "<p>new content</p>")
        timeline = build_timeline(versions)
        entry = timeline[0]
        self.assertEqual(entry["prompt_length"], len(entry["content_snapshot"]))

    def test_no_injection_score_field(self):
        versions = self._make_versions("old", "new text here")
        timeline = build_timeline(versions)
        self.assertNotIn("injection_score", timeline[0])

    def test_summary_initialized_to_none(self):
        versions = self._make_versions("old", "new text here")
        timeline = build_timeline(versions)
        self.assertIsNone(timeline[0]["summary"])

    def test_empty_diff_excluded(self):
        """Entries with no diff should not appear in timeline."""
        versions = self._make_versions("same content", "same content")
        timeline = build_timeline(versions)
        self.assertEqual(len(timeline), 0)


if __name__ == "__main__":
    unittest.main()
