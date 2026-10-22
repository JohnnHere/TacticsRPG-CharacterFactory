// Importador opcional. Copiar para Unity apenas junto do pacote autorizado.
// Ajusta PNGs com factory-manifest.json ao lado da raiz do personagem; preserva GUIDs.
using System.IO;
using UnityEditor;
using UnityEngine;

public sealed class CharacterFactoryImporter : AssetPostprocessor
{
    void OnPreprocessTexture()
    {
        const string prefix = "Assets/Resources/Characters/";
        if (!assetPath.StartsWith(prefix, System.StringComparison.Ordinal) ||
            !assetPath.EndsWith(".png", System.StringComparison.OrdinalIgnoreCase)) return;
        string relative = assetPath.Substring(prefix.Length);
        int slash = relative.IndexOf('/');
        if (slash < 1) return;
        string root = prefix + relative.Substring(0, slash);
        if (!File.Exists(root + "/factory-manifest.json")) return;
        var importer = (TextureImporter)assetImporter;
        importer.textureType = TextureImporterType.Sprite;
        importer.spriteImportMode = SpriteImportMode.Single;
        importer.spritePixelsPerUnit = 100;
        importer.filterMode = FilterMode.Point;
        importer.mipmapEnabled = false;
        importer.alphaIsTransparency = true;
        importer.textureCompression = TextureImporterCompression.Uncompressed;
        importer.npotScale = TextureImporterNPOTScale.None;
        var settings = new TextureImporterSettings();
        importer.ReadTextureSettings(settings);
        settings.spriteAlignment = (int)SpriteAlignment.Custom;
        settings.spritePivot = new Vector2(0.5f, 0f);
        importer.SetTextureSettings(settings);
    }
}
