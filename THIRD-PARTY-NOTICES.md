# Third-party review

Checked 2026-11-09 against installed manifests and LICENSE/NOTICE files.

- Playwright 1.62.1 and playwright-core 1.62.1 declare Apache-2.0. Their full installed LICENSE and NOTICE files are copied under LICENSES/third-party/ for reference. Package code and browser binaries are not bundled.
- Bundled/transitive components can have additional notices. These root Apache files are not an exhaustive inventory of every component. If distributing dependencies, preserve the exact package's ThirdPartyNotices.txt and all applicable notices.
- Python and Node.js runtimes are not bundled. Python uses PSF licensing; Node.js uses MIT with separately licensed third-party components.
- Chrome/Chromium is not bundled. Chrome has Google terms and third-party notices; Chromium is not entirely covered by a single license. Review the exact browser distribution before redistribution.
- Fonts are not bundled. Noto packages commonly use SIL OFL; verify exact package notices. System fonts may be proprietary and must not be copied without rights.
- No WeasyPrint/PyMuPDF dependency or PDF renderer is included. The separate internal PDF edition is unchanged and not relicensed here.
- Examples contain project introduction text, not an external article. Future source articles, user inputs and external assets retain their own rights.

The project licenses do not replace or restrict third-party licenses. Installation may contact package/vendor servers; rendering itself blocks network requests.

References:
https://github.com/microsoft/playwright
https://github.com/microsoft/playwright/blob/main/LICENSE
https://www.python.org/psf/license/
https://github.com/nodejs/node/blob/main/LICENSE
https://www.chromium.org/chromium-os/licenses/

The installed Playwright optional macOS dependency fsevents 2.3.2 declares MIT; its LICENSE is included for reference. Both Playwright ThirdPartyNotices.txt files are also included unchanged. These notices do not bundle the actual dependency code.
