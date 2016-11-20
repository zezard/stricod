package com.stricod.gpslogger.stricodapi;

import java.io.BufferedInputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

import org.json.JSONException;
import org.json.JSONObject;

import android.os.AsyncTask;
import android.util.Log;

public class StricodAPI {
    private static final String TAG = "stricoAPI";
    private static String token = null;
    public static final String baseUrl = "http://stricod.tednoob.se:9000";

    public static String login(String username, String password) {
        try {
            return new Login().execute(username, password).get();
        } catch (Exception e) {
            Log.e(TAG, "Nope...");
            return null;
        }
    }

    private static String responseToString(BufferedInputStream in)
    {
        int numRead;
        final int bufferSize = 1024;
        byte[] buffer = new byte[bufferSize];
        StringBuilder sb = new StringBuilder();
        try{
            while ((numRead = in.read(buffer)) != -1) {
                sb.append(new String(buffer, 0, numRead));
            }
        }catch (Exception e){
            Log.e(TAG,"Could not marshall respone");
            return null;
        }
        return sb.toString();
    }
    private static JSONObject responseToJSON(BufferedInputStream in)
    {
        String response = responseToString(in);
        try {
            JSONObject js = new JSONObject(response);
            return js;
        } catch (JSONException e)
        {
            Log.e(TAG, "Could not deserialize JSON");
            return null;
        }
    }

    private static class Login extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... strings) {
            String username = strings[0];
            String password = strings[1];
            String payload = "{\"username\":\"tulvgard\",\"password\":\"foobar\"}";
            InputStream in = null;
            try {
                URL u = new URL(baseUrl + "/user/auth");
                HttpURLConnection conn = (HttpURLConnection)u.openConnection();
                conn.setRequestMethod("POST");
                conn.setDoOutput(true);
                conn.setDoInput(true);
                conn.setRequestProperty("Content-Type","application/json");
                conn.setRequestProperty("Accept-Encoding","Identity");
                DataOutputStream wr = new DataOutputStream(conn.getOutputStream());
                wr.writeBytes(payload);
                Log.d(TAG,""+conn.getResponseCode()+": "+conn.getResponseMessage());

                BufferedInputStream response = new BufferedInputStream(conn.getInputStream());
                JSONObject js = responseToJSON(response);
                String token = null;
                try{
                    token = js.getString("token");
                } catch(JSONException e) {
                    Log.e(TAG, "No such key in respone \"token\"");
                }
                Log.d(TAG,"Token: "+token);
            } catch (MalformedURLException m) {
                Log.e(TAG,"URL is wrong");
                return null;
            } catch (IOException e) {
                Log.e(TAG,"IO error: " + e.getMessage());
                return null;
            }
            return token;
        }
    }
}
