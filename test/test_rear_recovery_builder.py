import contextlib
import copy
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    'rear_review_builder', ROOT / 'tools' / 'build-rear-recovery-review.py')
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class RearReviewBuilderTests(unittest.TestCase):
    def cells(self):
        return [{'direction': d, 'action': a}
                for d in BUILDER.DIRECTIONS for a in BUILDER.ACTIONS]

    def test_exact_matrix_rejects_duplicate_cells(self):
        cells = self.cells()
        with self.assertRaisesRegex(ValueError, 'duplicate cell'):
            BUILDER.cell_map_for(cells + [cells[0]], 'fixture')

    def test_exact_matrix_rejects_missing_cells(self):
        with self.assertRaisesRegex(ValueError, 'missing cells'):
            BUILDER.cell_map_for(self.cells()[:-1], 'fixture')

    def test_exact_matrix_rejects_unknown_cells(self):
        with self.assertRaisesRegex(ValueError, 'unexpected'):
            BUILDER.cell_map_for(self.cells() + [
                {'direction': 'side', 'action': 'Idle'}], 'fixture')

    def test_build_uses_declared_baseline_and_weapon_sources(self):
        manifest = BUILDER.read_json(BUILDER.DEFAULT_MANIFEST)
        baseline = copy.deepcopy(manifest)
        baseline_cells = BUILDER.cell_map_for(baseline['cells'], 'baseline')
        before_clip = baseline_cells[('front_r', 'Sword')]['clipJson']
        baseline_cells[('back_r', 'Sword')]['clipJson'] = before_clip
        for cell in manifest['cells']:
            changed = (cell['direction'], cell['action']) == ('back_r', 'Sword')
            cell['isAffected'] = changed
            cell['status'] = 'ACTIVE_CANDIDATE' if changed else 'UNCHANGED_ALIAS'
        manifest['revision'] = 'isolated-review-fixture'
        manifest['eligibleForIntegration'] = False
        manifest.pop('technicalStatus', None)
        with tempfile.TemporaryDirectory(dir=ROOT / 'tmp') as temp:
            temp = Path(temp)
            weapon = BUILDER.read_json(ROOT / 'assets/weapons/recruit-sword/weapon.json')
            weapon['name'] = 'Fixture axe candidate'
            weapon_path = temp / 'weapon.json'
            weapon_path.write_text(json.dumps(weapon), encoding='utf-8')
            manifest['weaponDefinitions'] = {'Axe': str(weapon_path.relative_to(ROOT))}
            manifest['integrationReport'] = str(
                (temp / 'report.md').relative_to(ROOT))
            (temp / 'report.md').write_text('Fixture report', encoding='utf-8')
            candidate_path = temp / 'candidate.json'
            baseline_path = temp / 'baseline.json'
            candidate_path.write_text(json.dumps(manifest), encoding='utf-8')
            baseline_path.write_text(json.dumps(baseline), encoding='utf-8')
            output = temp / 'review'
            with contextlib.redirect_stdout(io.StringIO()):
                BUILDER.build_rear_recovery_review(
                    candidate_path, output, baseline_manifest_path=baseline_path)
            catalog = BUILDER.read_json(output / 'catalogo.json')
            self.assertEqual(catalog['revision'], 'isolated-review-fixture')
            self.assertEqual(catalog['technicalStatus'], 'NOT_VERIFIED')
            self.assertIs(catalog['eligibleForIntegration'], False)
            self.assertEqual(catalog['baselineManifestSource'],
                             str(baseline_path.relative_to(ROOT)))
            source_clip = BUILDER.read_json(ROOT / before_clip)
            with Image.open(ROOT / source_clip['frames'][0]['png']) as source:
                with Image.open(output / 'AntesDepois/back_r_Sword_baseline_strip.png') as strip:
                    self.assertEqual(strip.size, (256 * len(source_clip['frames']), 256))
                    self.assertEqual(strip.crop((0, 0, 256, 256)).tobytes(),
                                     source.convert('RGBA').tobytes())
            copied_weapon = output / 'Armas/Fixture axe candidate/Fixture axe candidate.png'
            self.assertEqual(copied_weapon.read_bytes(), (ROOT / weapon['sprite']).read_bytes())
            original_axe = BUILDER.read_json(ROOT / 'assets/weapons/militia-axe/weapon.json')
            self.assertEqual((output / 'Armas/Fixture axe candidate/Antes.png').read_bytes(),
                             (ROOT / original_axe['sprite']).read_bytes())
            page = (output / 'index.html').read_text(encoding='utf-8')
            self.assertIn('isolated-review-fixture', page)
            self.assertIn('false — não integrar nem promover sem autorização do criador', page)
            self.assertIn('versão anterior declarada', page)
            self.assertIn('Fixture axe candidate — antes/depois', page)
            self.assertIn('../report.md', page)


if __name__ == '__main__':
    unittest.main()
