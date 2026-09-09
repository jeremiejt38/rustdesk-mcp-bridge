# Workflow de développement — rustdesk-mcp-bridge

Ce projet suit le Kit Standards Projet (KSP) avec les adaptations ci-dessous.

## Branches et commits

`main` est la branche stable. Après validation locale complète, les changements sont commités et poussés directement sur `main`, sans pull request. Les commits suivent Conventional Commits et restent atomiques.

## Validation

Exécuter les commandes de `docs/TESTING.md` avant chaque commit direct. Ne pas affaiblir les tests pour masquer une régression.

## Releases

Les releases sont préparées manuellement depuis des commits validés sur `main`, avec mise à jour du changelog et création du tag `vX.Y.Z`. Aucune pull request de release n’est créée.

- `fix:` propose un patch.
- `feat:` propose une mineure.
- `BREAKING CHANGE:` ou `!` propose une majeure.
- Une majeure exige toujours l’accord explicite du mainteneur.

**Progression :** une mineure est suivie de ses patches jusqu'à la mineure suivante.
Exemple : `0.1.0 → 0.1.1 (patch) → 0.2.0 (mineure) → 1.0.0 (majeure)`.

## Sécurité et confidentialité

- Ne jamais commiter d’identifiants RustDesk, de mots de passe, de tokens ou de secrets.
- Les captures d’écran et données distantes transitent par le protocole RustDesk ; aucune capture sensible ne doit être stockée dans le repo.
- Les tests utilisent des mocks et des environnements temporaires ; jamais de connexion réelle à un bureau distant.
