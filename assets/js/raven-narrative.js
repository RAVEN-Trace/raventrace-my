(() => {
  if (window.__RAVEN_NARRATIVE_RUNTIME_DEPRECATED__) return;
  window.__RAVEN_NARRATIVE_RUNTIME_DEPRECATED__ = true;
  // Intentionally no-op. Narrative findings and source rows now live in static,
  // auditable HTML generated through the canonical CASEFILE / Narrative Audit build.
  // Runtime JavaScript must not add, replace or re-date factual case content.
})();
