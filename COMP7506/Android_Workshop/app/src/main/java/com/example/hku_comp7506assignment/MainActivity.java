package com.example.hku_comp7506assignment;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.CookieHandler;
import java.net.CookieManager;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.concurrent.Executor;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;

public class MainActivity extends Activity implements View

        .OnClickListener {

    EditText txt_UserName, txt_UserPW;
    Button btn_Login;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        btn_Login = (Button) findViewById(R.id.btn_Login);
        txt_UserName = (EditText) findViewById(R.id.txt_UserName);
        txt_UserPW = (EditText) findViewById(R.id.txt_UserPW);

        // Register the Login button to click listener
        // Whenever the button is clicked, onClick is called
        btn_Login.setOnClickListener(this);

        doTrustToCertificates();
        CookieHandler.setDefault(new CookieManager());
    }

    @Override
    public void onClick(View v) {
        if (v.getId() == R.id.btn_Login) {
            String uname = txt_UserName.getText().toString();
            String upassword = txt_UserPW.getText().toString();

            connect(uname, upassword);
        }
    }

    public String ReadBufferedHTML(BufferedReader reader, char[] htmlBuffer, int bufSz) throws java.io.IOException {
        htmlBuffer[0] = '\0';
        int offset = 0;
        do {
            int cnt = reader.read(htmlBuffer, offset, bufSz - offset);
            if (cnt > 0) {
                offset += cnt;
            } else {
                break;
            }
        } while (true);
        return new String(htmlBuffer);
    }

    public String getMoodleFirstPage(String userName, String userPW) {
        HttpURLConnection conn_portal = null;
        HttpURLConnection conn_moodle = null;

        final int HTML_BUFFER_SIZE = 2 * 1024 * 1024; // 2MB buffer size
        char[] htmlBuffer = new char[HTML_BUFFER_SIZE];

        try {
            URL url_portal = new URL("https://i.cs.hku.hk/~twchim/moodle/model.html");
            conn_portal = (HttpURLConnection) url_portal.openConnection();

            String urlParameters = "username=" + URLEncoder.encode(userName, "UTF-8") + "&password=" + URLEncoder.encode(userPW, "UTF-8");
            byte[] postData = urlParameters.getBytes(StandardCharsets.UTF_8);

            conn_portal.setDoOutput(true);
            conn_portal.setInstanceFollowRedirects(false); // handle redirects manually
            conn_portal.setRequestMethod("POST");
            conn_portal.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            conn_portal.setRequestProperty("charset", "utf-8");
            conn_portal.setRequestProperty("Content-Length", Integer.toString(postData.length));
            conn_portal.setUseCaches(false);

            try (OutputStream wr = conn_portal.getOutputStream()) {
                wr.write(postData);
            }

            // Check for redirect
            int responseCode = conn_portal.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_MOVED_TEMP
                    || responseCode == HttpURLConnection.HTTP_MOVED_PERM
                    || responseCode == HttpURLConnection.HTTP_SEE_OTHER) {

                // Get redirect url from "location" header field
                String newUrl = conn_portal.getHeaderField("Location");
                conn_moodle = (HttpURLConnection) new URL(newUrl).openConnection();

                BufferedReader in = new BufferedReader(
                        new InputStreamReader(conn_moodle.getInputStream()), HTML_BUFFER_SIZE);
                String HTMLSource = ReadBufferedHTML(in, htmlBuffer, HTML_BUFFER_SIZE);
                in.close();
                return HTMLSource;

            } else {
                // If it is not a redirect, read the response directly
                BufferedReader in = new BufferedReader(
                        new InputStreamReader(conn_portal.getInputStream()), HTML_BUFFER_SIZE);
                String HTMLSource = ReadBufferedHTML(in, htmlBuffer, HTML_BUFFER_SIZE);
                in.close();
                return HTMLSource;
            }
        } catch (Exception e) {
            e.printStackTrace();
            return "Error during Moodle page access: " + e.getMessage();
        } finally {
            if (conn_portal != null) {
                conn_portal.disconnect();
            }
            if (conn_moodle != null) {
                conn_moodle.disconnect();
            }
        }
    }

    // trusting all certificate
    public void doTrustToCertificates() {
        TrustManager[] trustAllCerts = new TrustManager[]{
                new X509TrustManager() {
                    public java.security.cert.X509Certificate[] getAcceptedIssuers() {
                        return null;
                    }

                    public void checkClientTrusted(java.security.cert.X509Certificate[] certs, String authType) {
                    }

                    public void checkServerTrusted(java.security.cert.X509Certificate[] certs, String authType) {
                    }
                }
        };
        try {
            // Install the all-trusting trust manager
            SSLContext sc = SSLContext.getInstance("SSL");
            sc.init(null, trustAllCerts, new java.security.SecureRandom());
            HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    protected void alert(String title, String mymessage) {
        new AlertDialog.Builder(this)
                .setMessage(mymessage)
                .setTitle(title)
                .setCancelable(true)
                .setNegativeButton(android.R.string.cancel,
                        new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int whichButton) {
                            }
                        }
                )
                .show();
    }

    public void parse_HTML_Source_and_Switch_Activity(String HTMLsource) {

        Pattern p_coursename = Pattern.compile("<h3 class=\"coursename\".*?>.*?>(.*?)</a>");
        Matcher m_course = p_coursename.matcher(HTMLsource);
        Pattern p_teachercandidates = Pattern.compile("<div class=\"teachers\">Teacher: <.*?>(.*?)</a>");
        Matcher m_teachercandidates = p_teachercandidates.matcher(HTMLsource);

        ArrayList<String> cname = new ArrayList<String>();
        ArrayList<String> cteachers = new ArrayList<String>();
        ArrayList<String> cteachersfinal = new ArrayList<String>();
        ArrayList<Integer> cnamePos = new ArrayList<Integer>();
        ArrayList<Integer> cteachersPos = new ArrayList<Integer>();
        ArrayList<Integer> cteachersIdx = new ArrayList<Integer>();

        while (m_course.find()) {
            String course_name = m_course.group(1);
            Integer pos = m_course.start();
            boolean flag = true;
            for (String sss : cname) {
                if (sss.equals(course_name)) {
                    flag = false;
                }
            }
            if (flag) {
                cname.add(course_name);
                cnamePos.add(pos);
            }
        }

        while (m_teachercandidates.find()) {
            String string_teachername = m_teachercandidates.group(1);
            // int nameStartPosition = string_teachername.indexOf(">")+1;
            // int nameEndPosition = string_teachername.indexOf("</a>");
            // String teacher_name = string_teachername.substring(nameStartPosition, nameEndPosition);
            cteachers.add(string_teachername);
            Integer pos = m_teachercandidates.start();
            cteachersPos.add(pos);
        }

        Intent intent = new Intent(getBaseContext(), CourseListActivity.class);

        int cIdx = 0;
        for (int i = 0; i < cteachersPos.size(); ) {
            int cpos0 = -1, cpos1 = -1;
            int tpos = cteachersPos.get(i);
            if (cIdx < cnamePos.size()) {
                cpos0 = cnamePos.get(cIdx);
            }
            if (cIdx + 1 < cnamePos.size()) {
                cpos1 = cnamePos.get(cIdx + 1);
            }
            if (cpos0 < 0 || tpos < cpos0) { /// a course with 2 teachers!? Assume the teacher belongs to the previous course
                cteachersIdx.add(cIdx - 1);
                i++;
            } else if (cpos1 < 0 || (cpos0 < tpos && cpos1 > tpos)) {
                cteachersIdx.add(cIdx);
                i++;
                cIdx++;
            } else { /// tpos > cpos1 ==> teacher belongs to next classes
                cIdx++;
            }
        }
        for (int i = 0; i < cname.size(); i++) {
            String tname = "";
            for (int j = 0; j < cteachersIdx.size(); j++) {
                int cidx = cteachersIdx.get(j);
                if (cidx == i) {
                    tname += cteachers.get(j);
                }
            }
            cteachersfinal.add(tname);
        }
        intent.putStringArrayListExtra("CourseName", cname);
        intent.putStringArrayListExtra("Teachers", cteachersfinal);
        startActivity(intent);
    }

    public void connect( final String userName, final String userPW ){
        final ProgressDialog pdialog = new ProgressDialog(this);

        pdialog.setCancelable(false);
        pdialog.setMessage("Logging in ...");
        pdialog.show();

        ExecutorService executor = Executors.newSingleThreadExecutor();
        Handler handler = new Handler(Looper.getMainLooper());
        executor.execute(new Runnable() {
            boolean success;
            String moodlePageContent;

            @Override
            public void run() {
                success = true;
                moodlePageContent = getMoodleFirstPage(userName, userPW);

                if( moodlePageContent.equals("Fail to login") )
                    success = false;

                handler.post(new Runnable() {
                    @Override
                    public void run() {
                        if (success) {
                            parse_HTML_Source_and_Switch_Activity(moodlePageContent);
                        } else {
                            alert("Error", "Fail to login");
                        }
                        pdialog.hide();
                    }
                });
            }
        });
    }
}