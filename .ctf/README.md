# `.ctf/` Directory Purpose

This directory stores **intermediate generation artifacts** that are used during lab creation but are **NOT part of the final lab deliverable**. The final lab is in `build/` and `tests/`.

## What Goes Here (Working Files During Generation)

### Phase 1 - Context Creation
- `.ctf/context/SCENARIO.md` - Generated scenario (input for Phase 2)
- `.ctf/context/FLAG.md` - Generated flag definition (input for Phase 2)
- `.ctf/LIBRARY_PAGE.md` - Source material for lab generation (if provided)

### Phase 3 - Review
- `.ctf/REVIEW.md` - Review findings and recommendations (input for Phase 4)
- `.ctf/GOOD.md` - Empty file marker indicating lab passed review (created if no issues)
- `.ctf/review_logs/` - Detailed review execution logs

### Phase 4 - Correction
- `.ctf/CORRECTION.md` - Correction notes and changes made
- `.ctf/correction_logs/` - Detailed correction execution logs
- `.ctf/GOOD.md` - Updated when lab is corrected and validated

### Phase 5 - Metadata
- `.ctf/metadata.json` - Final metadata for CTF platform

### Other Artifacts
- `.ctf/test_results/` - Test execution results and summaries
- `.ctf/timing_logs/` - Phase timing logs (if enabled)
- `.ctf/MAINTAINERS.md` - Internal guide for maintainers (not player-facing)

## What Does NOT Go Here
- Actual lab code (goes in `build/`)
- Test files (goes in `tests/`)
- Production compose files (goes at root: `docker-compose.yml`)


