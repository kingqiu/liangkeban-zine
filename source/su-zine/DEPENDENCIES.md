# Dependencies and licensing

Project licenses: PolyForm Noncommercial 1.0.0 for code/templates; CC BY-NC 4.0 for original documentation/example content. See LICENSE-SCOPE.md and LICENSES/. Noncommercial source-available, not OSI-defined open source. package.json remains private to prevent accidental npm publication.

Runtime:
- Python 3.10+: builder uses only the standard library. Python itself uses the PSF license.
- Node.js 20+: runtime, not bundled; Node.js and bundled components have their own notices.
- Playwright 1.62.1: Apache-2.0; https://github.com/microsoft/playwright/blob/main/LICENSE
- Chromium or installed Google Chrome: not bundled. Chromium has BSD-style and third-party licenses; Chrome has Google terms. Playwright's license does not cover every browser component.
- Chinese fonts: installed separately, not bundled. Noto fonts commonly use SIL OFL; verify the exact font package and its notices before redistribution. System fonts must not be copied into releases without permission.

There are no WeasyPrint or PyMuPDF runtime dependencies in this edition. The earlier PDF workflow remains outside this package; removing it here does not resolve licensing for that separate workflow.

No third-party article content is bundled. Introduction examples describe this project. Check source copyright, quotation scope, attribution and image rights for each real article. The original missing resources could not be audited; this package uses explicitly reconstructed replacements rather than claiming recovery.

npm install and browser installation may access package/vendor download servers. The actual rendering step blocks network requests and does not upload content.

Installed package verification: THIRD-PARTY-NOTICES.md.
