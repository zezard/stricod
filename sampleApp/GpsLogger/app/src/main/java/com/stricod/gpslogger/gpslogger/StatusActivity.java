package com.stricod.gpslogger.gpslogger;

import android.Manifest;
import android.content.Context;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.net.Uri;
import android.support.design.widget.TextInputEditText;
import android.support.v7.app.AppCompatActivity;
import android.support.v4.app.ActivityCompat;
import android.os.Bundle;
import android.content.Intent;
import android.util.Log;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

public class StatusActivity extends AppCompatActivity {

    private final String TAG = "STATUS";

    private class MyLocationListener implements LocationListener {

        @Override
        public void onLocationChanged(Location location) {
            Date date = new Date(location.getTime());
            SimpleDateFormat df = new SimpleDateFormat("dd-MM-yyy HH:mm:ss");
            String myLoc = "" + location.getLongitude() + " " + location.getLatitude() + "\n";
            Log.d(TAG, myLoc);
            TextView locationLog = (TextView) findViewById(R.id.locationLog);
            locationLog.append(df.format(date)+": "+myLoc);
        }

        @Override
        public void onStatusChanged(String s, int i, Bundle bundle) {

        }

        @Override
        public void onProviderEnabled(String s) {

        }

        @Override
        public void onProviderDisabled(String s) {

        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResult) {
        LocationManager locManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        MyLocationListener locListener = new MyLocationListener();
        try {
            locManager.requestLocationUpdates(
                    locManager.GPS_PROVIDER, 5000, 10, locListener);
        } catch (SecurityException se) {
            Log.e(TAG, "Could not access location manager: " + se.toString());
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_status);

        Intent intent = getIntent();
        String token = intent.getStringExtra(LoginActivity.TOKEN_MESSAGE);
        ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, 1);
    }
}
