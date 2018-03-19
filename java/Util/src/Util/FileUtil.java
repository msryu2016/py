package Util;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;

public class FileUtil {

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		
		FileUtil fu = new FileUtil();
		String filename = "C:\\git\\repo\\ff\\readme.md";
		
		fu.replaceFile(filename, "^^", "--");		
		/*
		String datename = fu.addDateToFile(filename);
		System.out.println(datename);
		
		System.out.println(fu.getExt(filename));
		List<String> l = null;		
		try {
			l = FileUtil.readToList(filename);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		Iterator<String> iter = l.iterator();
		while(iter.hasNext()) {
			System.out.println(iter.next());
		}
		List<File> p = new ArrayList<File>();
		List<String> ll = FileUtil.listFile(new File("c:\\git\\repo"));
//		List<String> ll = FileUtil.listFiles(new File("c:\\git"), "([^\\s]+(\\.(?i)(php|py))$)");
		
		Iterator<String> iter1 = ll.iterator();
		while(iter1.hasNext())
		{
			String f= (String)iter1.next();
			System.out.println(f);
		}
		*/
	}

	
	public static List<String> readToList(String filename) throws IOException{
		List<String> out = new ArrayList<String>();
		
		
		BufferedReader br = new BufferedReader(new FileReader(filename));
		String line;
		
		while ((line = br.readLine())!=null) {
			out.add(line);
		}
		br.close();
		return out;
	}
	
	public static Map<String, String> readPropToMap(String filename, String seq) throws Exception {
		Map<String, String> out = new HashMap<String, String>();
		BufferedReader br = new BufferedReader(new FileReader(filename));
		String line;
		
		while ((line = br.readLine())!=null) {
			if (line.charAt(0) == '#') continue;
			if (line.trim().length()==0) continue;
			String[] pot = line.split(seq);
			out.put(pot[0], pot[1]);
		}
		br.close();
		
		return out;
	}
	
	public static Properties readProp(String filename) throws Exception {
		Properties prop = new Properties();
		prop.load(new FileInputStream(filename));
		return prop;
	}
	
	public static void writeFile(String filename, String text) throws IOException {
		BufferedWriter out = new BufferedWriter(new FileWriter(new File(filename)));
		out.write(text);
		out.close();
	}
	
	public static void writeBytes(String filename, byte[] bytes) throws IOException {
		OutputStream bos = new BufferedOutputStream(new FileOutputStream(filename));
		InputStream is = new ByteArrayInputStream(bytes);
		
		int token = -1;
		while((token = is.read())!=-1){
			bos.write(token);
		}
		bos.flush();
		bos.close();
		is.close();
	}

	public List<File> readDirs(String dir) {
		List<File> out = new ArrayList<File>();
		File fdir = new File(dir);
		
		if (fdir != null && fdir.isDirectory() ) {
			
			File[] files = null;
			files = fdir.listFiles();
			
			if (files!=null)
			{
				for(int i=0; i<files.length; i++)
				{
					File tmp = files[i];
					
					if (tmp.isDirectory())
					{
						out.add(tmp);
					}
				}
			}
		}
		return out;
	}
	
	public boolean makeDirs(String path){
		File f = new File(path);		
		return f.mkdirs();
	}
	
	public String getExt(String filename) {	
		int dot = filename.lastIndexOf(".");
		return filename.substring(dot+1);		
	}

	public String getExtLastDot(String filename) {	
		int dot = filename.lastIndexOf(".");
		return filename.substring(dot);		
	}
	
	public String addDateToFile(String filename) {
		String ext = getExtLastDot(filename);
		return String.format("%s_%s%s", filename.replace(ext, ""),DateUtil.getNow(), ext);
	}
	
	public static Collection<File> listFileTree(File dir) {
		Set<File> fileTree = new HashSet<File>();
		if (dir==null || dir.listFiles()!=null) {
			return fileTree;
		}
		
		for (File entry: dir.listFiles()) {
			if (entry.isFile()) fileTree.add(entry);
			else fileTree.addAll(listFileTree(entry));
		}
		return fileTree;
	}
	
	public List<File> addFiles(List<File> files, File dir)
	{
	    if (files == null)
	        files = new LinkedList<File>();

	    if (!dir.isDirectory())
	    {
	        files.add(dir);
	        return files;
	    }

	    for (File file : dir.listFiles()){
	    	addFiles(files, file);
	    }
	    return files;
	}
	
	public static List<String> listFile(File folder) {
		List<String> filepathlist = new ArrayList<>();
		
		File[] files = folder.listFiles();
		
		for(File file:files) {
			if (file.isDirectory()) {
				listFile(file);
			}else {
				filepathlist.add(file.getPath());
			}
		}
		return filepathlist;
	}
	
	
	public static void replaceFile(String filename, String src, String tgr) throws IOException {
		
        try
        {
	        File file = new File(filename);
	        BufferedReader reader = new BufferedReader(new FileReader(file));
	        String line = "", oldtext = "";
	        while((line = reader.readLine()) != null)
	        {
	            oldtext += line.replace(src, tgr)+"\r\n" ;
	        }
	        reader.close();
	      
	        FileWriter writer = new FileWriter(filename);
	        writer.write(oldtext);
	        writer.close();
	    }
	    catch (IOException ioe)
	    {
	        ioe.printStackTrace();
	    }
	}
	
	/*
	public static List<String> listFiles(File folder, String regex) {
		List<String> filepathlist = new ArrayList<>();
		
		File[] files = folder.listFiles();
		
		for(File file:files) {
			if (file.isDirectory()) {
				listFiles(file);
			}else {
				String line = file.getPath();
				System.out.println("line:" + line);
				if (line.matches(regex)) {
					listFiles.add(file.getPath());
				}
			}
		}
		return filepathlist;
	}
	*/	
	/*
	public List<File> addFiles(List<File> files, File dir, String regex)
	{
	    if (files == null)
	        files = new LinkedList<File>();

	    if (!dir.isDirectory())
	    {
	        files.add(dir);
	        return files;
	    }
	    String line = null;
	    for (File file : dir.listFiles())
	    	line = file.getAbsolutePath();	    	
	    	if (line.matches(regex)) {
	    		addFiles(files, file, regex);
	    	}
	    return files;
	}	
	*/
}
