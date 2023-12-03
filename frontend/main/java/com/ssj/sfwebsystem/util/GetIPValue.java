package com.ssj.sfwebsystem.util;

import java.net.InetAddress;
import java.net.UnknownHostException;

public class GetIPValue {
    public static String getIPValue(){
        try {
            return InetAddress.getLocalHost().getHostAddress();
        } catch (UnknownHostException e) {
            e.printStackTrace();
        }
        return null;
    }
}
