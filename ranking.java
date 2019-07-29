import java.util.*;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.List; 
import java.util.ArrayList; 
import java.util.Iterator;
import java.util.HashMap;
import java.io.*;


public class ranking
{
    
    public static void main(String[] args)throws FileNotFoundException{
        String reportFile = "crawled_content.csv";
        //BufferedReader readFile = new BufferedReader(new FileReader(reportFile));
        ArrayList<String[]> mylist = new ArrayList<String[]>();
        String line, megaString = "";
        try (BufferedReader readFile = new BufferedReader(new FileReader(reportFile))) {
            
                while ((line = readFile.readLine()) != null) {
                String stuff[] = line.split(",");
                
                mylist.add(stuff);
                
                megaString = megaString + stuff[1] ;
                System.out.println(" " + megaString);
                //rank(stuff[1]);
                rank(megaString);
                //for(int i = 0; i < 2;i++){
                   //System.out.println( stuff[i] + " , contents=" + stuff[i+1] + "]");
                //}
            }
            
        }
        catch (IOException e)
        {
             e.printStackTrace();
        }
        catch(ArrayIndexOutOfBoundsException exception){
            System.out.print(" ");
        }
    }
    
    public static void rank(String s){ 
        String a[] = s.split(" ");
        HashMap<String, Integer> time = new HashMap<String, Integer>();
        HashMap<String, Integer> sorted = new HashMap<String, Integer>();
        int k = 0;
        int count; 
        while(k<a.length){
            count = 0;
            String dummy = a[k];
            for (int i = 0; i < a.length; i++)  
            { 
                
                if (dummy.equals(a[i])) {
                    count++; 
                }
                
                time.put(dummy,count);
                
            } 
            //System.out.println(time);
            k++;
        }
        sorted =sorting(time);
        System.out.println(sorted);
        table(sorted, k);
        writeToFile(sorted);
    }
    
    public static void table(HashMap<String, Integer> sorted, int N){
        // output Statement
        int r = 1;
        double Pr, rPr;
        double frequence; 
        for (String work : sorted.keySet()){
            frequence= sorted.get(work);
            Pr = (frequence / (double)N )* 100;
            rPr = (r*Pr)/ 100;
            System.out.println("Work: " + work + "\n"  + 
                               "frequence: " + frequence + "\n" +
                               "Rank: " + r + "\n");
                              // "Pr: " + Pr + "\n" + 
                               //"rPr: " + rPr +"\n\n");
                           
            r++;
        }
        
   } 
   
   public static void writeToFile(HashMap<String, Integer> sorted) 
   { 
      // File file = new File("./plot.cvs"); 
      try (PrintWriter writer = new PrintWriter(new File("./plot.csv"))) {
    
          StringBuilder sb = new StringBuilder();
          for(String word: sorted.keySet()){
            int frequence= sorted.get(word);
            sb.append(word);
            sb.append(',');
            sb.append(frequence);
            sb.append('\n');
         }
          
    
          writer.write(sb.toString());
    
          System.out.println("done!");
    
        } catch (FileNotFoundException e) {
          System.out.println(e.getMessage());
        }
    }
   
   public static HashMap<String, Integer> sorting (HashMap<String, Integer> temp) 
    { 
        // Create a list from elements of HashMap 
        List<Map.Entry<String, Integer> > list =  new LinkedList<Map.Entry<String, Integer> >(temp.entrySet()); 
  
        // Sort the list 
        Collections.sort(list, new Comparator<Map.Entry<String, Integer> >() 
        { 
            public int compare(Map.Entry<String, Integer> o1,  
                               Map.Entry<String, Integer> o2) 
            { 
                return (o2.getValue()).compareTo(o1.getValue()); 
            } 
        }); 
          
        // put data from sorted list to hashmap  
        HashMap<String, Integer> sorted = new LinkedHashMap<String, Integer>(); 
        for (Map.Entry<String, Integer> aa : list) { 
            sorted.put(aa.getKey(), aa.getValue()); 
        } 
        return sorted; 
    } 
   } 
