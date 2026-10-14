# Catalyst Capital Management | Residential Lending Site

Static website for Catalyst Capital Management's residential construction, fix-and-flip and bridge lending platform. Plain HTML, CSS and JavaScript, deployed on Netlify with no build step.

## Pages

| Path | Page |
|---|---|
| `/` | Home: program tabs, highlights, project types, loan estimator, recent closings, process, FAQ |
| `/construction-loans/` | Ground-Up Construction program |
| `/fix-and-flip-loans/` | Fix & Flip program |
| `/bridge-loans/` | Bridge program (acquisition, refinance, entitled land) |
| `/how-it-works/` | Loan process, draw process, program comparison, document checklist |
| `/faq/` | Full FAQ |
| `/about/` | Company, approach, leadership |
| `/contact/` | Contact details and contact form |
| `/apply/` | Three-step online application (Netlify Forms, with file uploads) |
| `/thank-you/` | Form confirmation |

## Editing

Pages are generated from `_src/pages/*.html` by `_src/build.py`, which adds the shared header, footer, estimator widget and closing call to action.

1. Edit a page in `_src/pages/`, or the header and footer in `_src/build.py`.
2. Run `python3 _src/build.py` (Python 3, no dependencies).
3. Commit both the `_src` change and the regenerated HTML.

Program limits used by the loan estimator and the application's LTC/LTV checks live in one place: the `PROGRAMS` object at the top of `assets/js/site.js`.

## Forms

Two Netlify Forms are detected automatically on deploy:

- `loan-application`: the online application, including two optional file uploads (8 MB combined).
- `contact`: the contact form.

After the first deploy, set email notifications in Netlify under **Site configuration → Forms → Form notifications**. Both forms use a honeypot field for spam filtering.

## Deploy on Netlify

1. In Netlify, choose **Add new site → Import an existing project → GitHub** and select `catalystccm3`.
2. Leave the build command empty and the publish directory as `.` (already set in `netlify.toml`).
3. Add the custom domain, then update `SITE` in `_src/build.py`, `robots.txt` and `sitemap.xml` if it differs from `lending.catalystccm.com`.

## Brand

Catalyst Navy `#0E1A3D`, Catalyst Gold `#B79A4F`, Aptos (with Calibri and system fallbacks). Logos in `assets/img/` are web versions of the official brand files. Photography is generic stock from Unsplash, loaded from Unsplash's image CDN under the Unsplash License.
