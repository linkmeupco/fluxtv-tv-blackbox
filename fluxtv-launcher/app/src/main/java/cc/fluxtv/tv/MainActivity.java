package cc.fluxtv.tv;

import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.view.KeyEvent;

/**
 * FluxTV Android TV — Launcher Activity
 *
 * Strategy: open fluxtv.cc in the system browser (Chrome / Chromium for Android TV).
 * This gives us:
 *   - Full Chrome WebEngine (no WebView limitations)
 *   - Hardware-accelerated HLS/DASH video via the browser's native media stack
 *   - No CORS issues (browser handles it natively)
 *   - Widevine DRM at L1 level (same as the browser)
 *   - D-pad navigation that Chrome for Android TV already handles
 *   - Auto-updates as Chrome updates — no APK maintenance
 *
 * The APK itself only serves as the Android TV home-screen entry point
 * (banner + Leanback launcher category) so your friends can find it easily.
 */
public class MainActivity extends Activity {

    private static final String FLUXTV_URL = "https://fluxtv.cc/";

    // Chrome and common Android TV browser package names, in preference order
    private static final String[] BROWSER_PACKAGES = {
        "com.android.chrome",
        "com.chrome.beta",
        "com.chrome.dev",
        "org.chromium.chrome",           // Chromium forks on TV boxes
        "com.ksmobile.newbrowser",
        "com.opera.browser",
        "org.mozilla.firefox",
        "com.microsoft.emmx",            // Edge
        "com.android.browser",           // Stock Android browser fallback
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Try to open in the best available browser
        if (!openInBrowser()) {
            // Last resort: fire a generic VIEW intent and let Android pick
            Intent fallback = new Intent(Intent.ACTION_VIEW, Uri.parse(FLUXTV_URL));
            fallback.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            startActivity(fallback);
        }

        // Close the launcher shell — the browser is now the foreground app
        finish();
    }

    /**
     * Tries each known browser in priority order.
     * Returns true if one was launched, false if none found.
     */
    private boolean openInBrowser() {
        PackageManager pm = getPackageManager();

        for (String pkg : BROWSER_PACKAGES) {
            try {
                // Check the package is actually installed
                pm.getPackageInfo(pkg, 0);

                Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(FLUXTV_URL));
                intent.setPackage(pkg);
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);

                startActivity(intent);
                return true;
            } catch (PackageManager.NameNotFoundException ignored) {
                // This browser isn't installed — try next
            } catch (Exception ignored) {
                // Intent failed — try next
            }
        }
        return false;
    }
}
