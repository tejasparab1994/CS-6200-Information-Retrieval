import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

import java.io.*;
import java.util.ArrayList;
import java.util.Scanner;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */
public class HW4 {
    private static Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_47);
    private static Analyzer sAnalyzer = new SimpleAnalyzer(Version.LUCENE_47);

    private IndexWriter writer;
    private ArrayList<File> queue = new ArrayList<File>();

    public static void main(String[] args) throws IOException {
        System.out
                .println("Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\\temp\\index)");

        String indexLocation = null;
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();

        HW4 indexer = null;
        try {
            indexLocation = s;
            indexer = new HW4(s);
        } catch (Exception ex) {
            System.out.println("Cannot create index..." + ex.getMessage());
            System.exit(-1);
        }

        // ===================================================
        // read input from user until he enters q for quit
        // ===================================================
        while (!s.equalsIgnoreCase("q")) {
            try {
                System.out
                        .println("Enter the FULL path to add into the index (q=quit): (e.g. /home/mydir/docs or c:\\Users\\mydir\\docs)");
                System.out
                        .println("[Acceptable file types: .xml, .html, .html, .txt]");
                s = br.readLine();
                if (s.equalsIgnoreCase("q")) {
                    break;
                }

                // try to add file into the index
                indexer.indexFileOrDirectory(s);
            } catch (Exception e) {
                System.out.println("Error indexing " + s + " : "
                        + e.getMessage());
            }
        }

        // ===================================================
        // after adding, we always have to call the
        // closeIndex, otherwise the index is not created
        // ===================================================
        indexer.closeIndex();

        // =========================================================
        // Now search
        // =========================================================

        Scanner sc = new Scanner(new File("/Users/tejasparab/Desktop/queries.txt"));
        ArrayList<String> list = new ArrayList<String>();
        while (sc.hasNextLine()) {
            list.add(sc.nextLine());
        }
        System.out.println(list);
        int file_count = 1;
        int q_id = 1;
        for(String query_val: list)
        {
            System.out.println(query_val);
            IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(indexLocation)));
            IndexSearcher searcher = new IndexSearcher(reader);
            TopScoreDocCollector collector = TopScoreDocCollector.create(100, true);

            try {
                Query q = new QueryParser(Version.LUCENE_47, "contents", analyzer).parse(query_val);
                searcher.search(q, collector);
                ScoreDoc[] hits = collector.topDocs().scoreDocs;

                // 4. display results
                FileWriter fileWriter = new FileWriter(Integer.toString(file_count) + ".txt");
                BufferedWriter bufferedWriter = new BufferedWriter(fileWriter);
                bufferedWriter.write("query_id Q0 doc_id rank BM25_score system_name");
                bufferedWriter.newLine();
                System.out.println("Found " + hits.length + " hits.");
                for (int i = 0; i < hits.length; ++i) {
                    int docId = hits[i].doc;
                    Document d = searcher.doc(docId);
                    System.out.println(q_id + " " + "Q0" + " " + d.get("filename") + " " + (i + 1) + ". "
                            + " score=" + hits[i].score + " " + "UniBM25");
                    bufferedWriter.write(q_id + " " + "Q0" + " " + d.get("filename") + " " + (i + 1) + ". "
                            + " score=" + hits[i].score + " " + "UniBM25");
                    bufferedWriter.newLine();
                }
                bufferedWriter.close();
                file_count++;
                q_id ++;
            }

            catch (Exception e) {
                System.out.println("Error searching " + query_val + " : "
                        + e.getMessage());
                break;
            }

        }
    }


    /**
     * Constructor
     *
     * @param indexDir
     *            the name of the folder in which the index should be created
     * @throws java.io.IOException
     *             when exception creating index.
     */
    HW4(String indexDir) throws IOException {

        FSDirectory dir = FSDirectory.open(new File(indexDir));

        IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47,analyzer);

        writer = new IndexWriter(dir, config);
    }

    /**
     * Indexes a file or directory
     *
     * @param fileName
     *            the name of a text file or a folder we wish to add to the
     *            index
     * @throws java.io.IOException
     *             when exception
     */
    public void indexFileOrDirectory(String fileName) throws IOException {
        // ===================================================
        // gets the list of files in a folder (if user has submitted
        // the name of a folder) or gets a single file name (is user
        // has submitted only the file name)
        // ===================================================
        addFiles(new File(fileName));

        int originalNumDocs = writer.numDocs();
        for (File f : queue) {
            FileReader fr = null;
            try {
                Document doc = new Document();

                // ===================================================
                // add contents of file
                // ===================================================
                fr = new FileReader(f);
                doc.add(new TextField("contents", fr));
                doc.add(new StringField("path", f.getPath(), Field.Store.YES));
                doc.add(new StringField("filename", f.getName(),
                        Field.Store.YES));

                writer.addDocument(doc);
                System.out.println("Added: " + f);
            } catch (Exception e) {
                System.out.println("Could not add: " + f);
            } finally {
                fr.close();
            }
        }

        int newNumDocs = writer.numDocs();
        System.out.println("");
        System.out.println("************************");
        System.out
                .println((newNumDocs - originalNumDocs) + " documents added.");
        System.out.println("************************");

        queue.clear();
    }

    private void addFiles(File file) {

        if (!file.exists()) {
            System.out.println(file + " does not exist.");
        }
        if (file.isDirectory()) {
            for (File f : file.listFiles()) {
                addFiles(f);
            }
        } else {
            String filename = file.getName().toLowerCase();
            // ===================================================
            // Only index text files
            // ===================================================
            if (filename.endsWith(".htm") || filename.endsWith(".html")
                    || filename.endsWith(".xml") || filename.endsWith(".txt")) {
                queue.add(file);
            } else {
                System.out.println("Skipped " + filename);
            }
        }
    }

    /**
     * Close the index.
     *
     * @throws java.io.IOException
     *             when exception closing
     */
    public void closeIndex() throws IOException {
        writer.close();
    }
}
