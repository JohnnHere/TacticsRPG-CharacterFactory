# Narrow integration correction by root

Root verified first two rejected inpaint jobs via READ ONLY PixelLab get_image on 2026-10-26 (no generation). Actual IDs: af1e7ba8-655e-45fd-9798-2ba4b8cda7e9 and ed109b13-7b60-4200-8a43-ed8a9fb8f561. Both completed, charged_generations=6 each. Prior ledger had incorrect UUID suffixes and nonexistent request/output paths.

Completion metadata is saved in raw/root-cost-confirmation-k1.json and k2.json. Existing original creation/request JSONs copied unchanged from tmp/inpaint_walk_k[12]_{req,res}.json into raw/walk-draft01-k[12]-{request,creation}.json. Ledger first2records corrected to actualIDs, existingPNGoutputs and completionReceipt. All current ledger input/output/evidence paths resolve. Root authored NO new production art; only metadata verification and this narrow integration fix. Subsequent production updates must preserve corrected provenance.
