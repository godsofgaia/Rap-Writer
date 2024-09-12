from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass

    def check_and_request_permissions():
        """Checks and requests necessary permissions for the app."""
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        ActivityCompat = autoclass('androidx.core.app.ActivityCompat')
        PackageManager = autoclass('android.content.pm.PackageManager')

        permissions = [
            'android.permission.INTERNET',
            'android.permission.WRITE_EXTERNAL_STORAGE',
            'android.permission.READ_EXTERNAL_STORAGE'
        ]

        permission_results = {}
        for permission in permissions:
            result = ActivityCompat.checkSelfPermission(
                PythonActivity.mActivity, permission)
            permission_results[permission] = result

        permissions_to_request = [
            perm for perm, result in permission_results.items()
            if result != PackageManager.PERMISSION_GRANTED
        ]

        if permissions_to_request:
            ActivityCompat.requestPermissions(
                PythonActivity.mActivity,
                permissions_to_request,
                1  # Request code
            )
        else:
            print("All permissions are already granted.")

else:
    def check_and_request_permissions():
        """No permissions needed for non-Android platforms."""
        print("Permissions are not required on non-Android platforms.")