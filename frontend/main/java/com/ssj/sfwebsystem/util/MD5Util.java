package com.ssj.sfwebsystem.util;

import java.security.MessageDigest;

/**
 * MD5加密工具包
 */
public class MD5Util {
    private static final String hexDigits[] = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
            "a", "b", "c", "d", "e", "f"};

    /**
     * 对用户的密码进行MD5加密
     * @param origin
     * @param charsetName
     * @return
     */
    public static String MD5EnCode(String origin, String charsetName){
        String resultString = null;
        try{
            resultString = new String(origin);
            MessageDigest md = MessageDigest.getInstance("MD5");
            if(charsetName == null || "".equals(charsetName)) {
                resultString = byteArrayToHexString(md.digest(resultString.getBytes()));
            }else{
                resultString = byteArrayToHexString(md.digest(resultString.getBytes(charsetName)));
            }
        }catch (Exception e){
        }
        return resultString;
    }

    private static String byteArrayToHexString(byte[] b){
        StringBuffer stringBuffer = new StringBuffer();
        for(int i = 0; i < b.length; i++){
            stringBuffer.append(byteToHexString(b[i]));
        }
        return stringBuffer.toString();
    }

    private static String byteToHexString(byte b){
        int n = b;
        if(n < 0)
            n += 256;
        int d1 = n / 16;
        int d2 = n % 16;
        return hexDigits[d1] + hexDigits[d2];
    }
}
