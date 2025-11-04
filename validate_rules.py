#!/usr/bin/env python3
"""
Script de validation des règles Cursor CLI
Vérifie que tous les fichiers .mdc dans .cursor/rules sont bien formatés
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

class RuleValidator:
    def __init__(self, rules_dir: str = ".cursor/rules"):
        self.rules_dir = Path(rules_dir)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.stats = {
            "total_files": 0,
            "valid_files": 0,
            "invalid_files": 0,
            "files_without_description": 0,
            "files_without_alwaysApply": 0,
            "files_with_invalid_yaml": 0,
        }
    
    def validate_file(self, file_path: Path) -> Tuple[bool, Dict]:
        """Valide un fichier de règle individuel"""
        self.stats["total_files"] += 1
        
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            self.errors.append(f"❌ {file_path}: Impossible de lire le fichier - {e}")
            self.stats["invalid_files"] += 1
            return False, {}
        
        # Vérifier la présence du frontmatter
        if not content.startswith("---"):
            self.errors.append(f"❌ {file_path}: Manque le frontmatter YAML (doit commencer par '---')")
            self.stats["invalid_files"] += 1
            return False, {}
        
        # Extraire le frontmatter
        frontmatter_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if not frontmatter_match:
            self.errors.append(f"❌ {file_path}: Frontmatter YAML mal formaté (doit être délimité par '---')")
            self.stats["invalid_files"] += 1
            return False, {}
        
        frontmatter_str = frontmatter_match.group(1)
        
        # Parser le YAML basique (sans dépendance externe)
        frontmatter = {}
        has_yaml_errors = False
        
        # Extraire les propriétés clés avec regex
        description_match = re.search(r'^description:\s*(.+)$', frontmatter_str, re.MULTILINE)
        if description_match:
            desc_value = description_match.group(1).strip()
            # Enlever les guillemets si présents
            if desc_value.startswith('"') and desc_value.endswith('"'):
                desc_value = desc_value[1:-1]
            elif desc_value.startswith("'") and desc_value.endswith("'"):
                desc_value = desc_value[1:-1]
            frontmatter["description"] = desc_value
        else:
            frontmatter["description"] = None
        
        always_apply_match = re.search(r'^alwaysApply:\s*(true|false)$', frontmatter_str, re.MULTILINE | re.IGNORECASE)
        if always_apply_match:
            frontmatter["alwaysApply"] = always_apply_match.group(1).lower() == "true"
        else:
            frontmatter["alwaysApply"] = None
        
        # Vérifier globs (peut être une liste multi-lignes)
        globs_match = re.search(r'^globs:\s*\[(.*?)\]', frontmatter_str, re.MULTILINE | re.DOTALL)
        if globs_match:
            globs_str = globs_match.group(1).strip()
            if globs_str:
                # Extraire les éléments de la liste
                globs_items = re.findall(r'["\']([^"\']+)["\']', globs_str)
                frontmatter["globs"] = globs_items
            else:
                frontmatter["globs"] = []
        else:
            globs_simple = re.search(r'^globs:\s*\[?\s*\]', frontmatter_str, re.MULTILINE)
            if globs_simple:
                frontmatter["globs"] = []
            else:
                frontmatter["globs"] = None
        
        # Vérifier les propriétés obligatoires
        has_errors = False
        
        if frontmatter["description"] is None:
            self.errors.append(f"❌ {file_path}: Manque la propriété 'description' (obligatoire)")
            self.stats["files_without_description"] += 1
            has_errors = True
        elif not frontmatter["description"] or not frontmatter["description"].strip():
            self.errors.append(f"❌ {file_path}: La propriété 'description' est vide")
            has_errors = True
        
        if frontmatter["alwaysApply"] is None:
            self.errors.append(f"❌ {file_path}: Manque la propriété 'alwaysApply' (obligatoire)")
            self.stats["files_without_alwaysApply"] += 1
            has_errors = True
        
        # Vérifier que 'globs' est une liste si présent (déjà fait par le parsing)
        if frontmatter["globs"] is not None and not isinstance(frontmatter["globs"], list):
            self.errors.append(f"❌ {file_path}: 'globs' doit être une liste")
            has_errors = True
        
        # Vérifier qu'il y a du contenu après le frontmatter
        content_after = content[frontmatter_match.end():].strip()
        if not content_after:
            self.warnings.append(f"⚠️  {file_path}: Aucun contenu après le frontmatter")
        
        if has_errors:
            self.stats["invalid_files"] += 1
            return False, frontmatter
        
        self.stats["valid_files"] += 1
        return True, frontmatter
    
    def validate_all(self) -> bool:
        """Valide tous les fichiers .mdc dans le répertoire des règles"""
        if not self.rules_dir.exists():
            self.errors.append(f"❌ Le répertoire {self.rules_dir} n'existe pas")
            return False
        
        # Trouver tous les fichiers .mdc
        mdc_files = list(self.rules_dir.rglob("*.mdc"))
        
        if not mdc_files:
            self.errors.append(f"❌ Aucun fichier .mdc trouvé dans {self.rules_dir}")
            return False
        
        print(f"📋 Validation de {len(mdc_files)} fichiers de règles...\n")
        
        # Valider chaque fichier
        for file_path in sorted(mdc_files):
            is_valid, frontmatter = self.validate_file(file_path)
            if is_valid:
                always_apply = frontmatter.get("alwaysApply", False)
                status = "✅" if always_apply else "ℹ️ "
                desc = frontmatter.get("description", "")[:60]
                print(f"{status} {file_path.relative_to(self.rules_dir)}")
                if desc:
                    print(f"   Description: {desc}...")
        
        return len(self.errors) == 0
    
    def print_report(self):
        """Affiche le rapport de validation"""
        print("\n" + "="*70)
        print("📊 RAPPORT DE VALIDATION")
        print("="*70)
        
        print(f"\n📈 Statistiques:")
        print(f"   Total de fichiers: {self.stats['total_files']}")
        print(f"   ✅ Fichiers valides: {self.stats['valid_files']}")
        print(f"   ❌ Fichiers invalides: {self.stats['invalid_files']}")
        
        if self.stats['files_without_description'] > 0:
            print(f"   ⚠️  Sans description: {self.stats['files_without_description']}")
        if self.stats['files_without_alwaysApply'] > 0:
            print(f"   ⚠️  Sans alwaysApply: {self.stats['files_without_alwaysApply']}")
        if self.stats['files_with_invalid_yaml'] > 0:
            print(f"   ⚠️  YAML invalide: {self.stats['files_with_invalid_yaml']}")
        
        if self.errors:
            print(f"\n❌ ERREURS ({len(self.errors)}):")
            for error in self.errors:
                print(f"   {error}")
        
        if self.warnings:
            print(f"\n⚠️  AVERTISSEMENTS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   {warning}")
        
        if not self.errors and not self.warnings:
            print("\n✅ Toutes les règles sont correctement configurées et lisibles par Cursor CLI!")
        elif not self.errors:
            print("\n✅ Toutes les règles sont valides (avec quelques avertissements)")
        else:
            print("\n❌ Des erreurs doivent être corrigées")
        
        print("="*70)

def main():
    validator = RuleValidator()
    is_valid = validator.validate_all()
    validator.print_report()
    
    # Code de sortie
    exit(0 if is_valid else 1)

if __name__ == "__main__":
    main()

