## GH Artifact Contract

- Apply this contract only when the repo has an external artifact, the current change affects a releasable artifact, or the final answer makes an artifact or no-artifact claim.
- Identify the real deliverable from the project instead of forcing Docker, PyPI, or any other registry by default.
- Capture or verify the artifact identity, registry target, version source, release policy, tag style, changelog or release-note source, and post-publish consumer check.
- In audit-only flows, verify and classify artifact state; do not publish or mutate registry artifacts unless the workflow explicitly moves into a ship or publish skill.
- Build, package, install, pull, run, or consume local artifacts enough to catch packaging and runtime failures before publishing or before making a local artifact-health claim.
- Publish external artifacts only when repo policy and the merged change require a release, tag, package, image, module, binary, or other public artifact.
- Derive versions from trustworthy project metadata and tag history instead of inventing semantics.
- Verify live release and registry endpoints after publishing or when auditing artifact state, including tags, digests, package pages, release pages, and published artifacts.
- For PyPI publishes, prefer Trusted Publishing or another short-lived identity path over repository-stored long-lived tokens when supported, build the intended sdist and wheel, publish the intended version, verify the live PyPI version, install that exact version from PyPI locally, and run the smoke or documented consumer check against the published artifact instead of an editable checkout.
- For PyPI publishes that emit attestations or provenance, verify the metadata through PyPI or the selected verifier instead of relying only on upload success.
- For Docker or OCI image publishes, build locally, run a smoke test, publish the intended tags or digests, verify the live registry state, and pull or consume the published image when relevant.
