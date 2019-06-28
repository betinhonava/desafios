package idwall.desafio.string;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by Rodrigo Catão Araujo on 06/02/2018.
 */
public class IdwallFormatter extends StringFormatter {

    public IdwallFormatter(int limit, boolean justify) {
        super(limit, justify);
    }

    /**
     * Should format as described in the challenge
     *
     * @param text
     * @return
     */
    @Override
    public String format(String text) {
        StringBuilder builder = new StringBuilder();
        String[] paragraphs = text.split("\\n");
        for (String paragraph : paragraphs) {
            List<String> wordList = new ArrayList<>();
            int space_index = 0;
            int end = 0;
            do {
                int start = space_index;
                end = paragraph.indexOf(" ", start + 1) > 0 ? paragraph.indexOf(" ", start + 1) : paragraph.length();
                wordList.add(paragraph.substring(start, end));
                wordList.add(" ");
                space_index = paragraph.indexOf(" ", end) + 1;
            } while (end < paragraph.length());
            int letter_count = 0;
            for (String word : wordList) {
                letter_count += word.length();
                if (letter_count <= this.limit) {
                    builder.append(word);
                } else {
                    builder.append("\n");
                    if (!word.equals(" ")) {
                        builder.append(word);
                    }
                    letter_count = word.length();
                }
            }
            builder.append("\n");
        }
        if (this.justify) {
            String[] lines = builder.toString().split("\\n");
            builder = new StringBuilder();
            for (String line : lines) {
                String[] wordList = line.split("\\s");
                int letterCount = 1;
                for (String word : wordList) {
                    letterCount += word.length();
                }
                int numSpaces = (int) Math.floor((this.limit - letterCount) / (wordList.length - 1));
                int extraSpaces = this.limit - letterCount - (wordList.length - 1) * numSpaces;
                for (int i = 0; i < wordList.length; i++) {
                    String span = "";
                    for (int j = 0; j < numSpaces; j++) {
                        span += " ";
                    }
                    if (i < extraSpaces) {
                        span += " ";
                    }
                    builder.append(wordList[i]);
                    if (i < wordList.length - 1) {
                        builder.append(span);
                    }
                }
                if (wordList.length == 0) {
                    builder.append("\n ");
                }
                builder.append("\n");
            }
        }
        return builder.toString();
    }

}
