package Util;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class DateUtil {
	
	public static void main(String[] args) {
		DateUtil d = new DateUtil();
		System.out.println(DateUtil.getNow("yyyyMMdd"));
	}
	
	public static String getNow(String skin){
		Date today = new Date();
		Locale lo = new Locale("KOREAN", "KOREA");
		SimpleDateFormat f = new SimpleDateFormat(skin, lo);
		return f.format(today);
	}
	
	public static String getNow() {
		return DateUtil.getNow("yyyyMMdd");
	}

}
