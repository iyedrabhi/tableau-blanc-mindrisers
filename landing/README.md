Cure & Simple — Landing Page

Files:
- `index.html` — static landing page
- `styles.css` — page styles

Preview locally:
1. Open the `landing` folder in a browser directly, or run a simple HTTP server:

PowerShell:
```powershell
cd "C:\Users\lenovo\Desktop\projet_GL\landing"
python -m http.server 8000
Start-Process 'http://127.0.0.1:8000'
```

2. The page uses external images (Unsplash) and Google Fonts; ensure you have internet access.

Notes:
- This is a static mockup. If you want it integrated into Django templates, I can move `index.html` into your app's templates and wire a view.
- If you want placeholder images replaced with local assets, I can add them to the `landing/static` folder.
