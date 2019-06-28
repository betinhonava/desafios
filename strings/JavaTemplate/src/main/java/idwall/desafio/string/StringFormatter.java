package idwall.desafio.string;

/**
 * Created by Rodrigo Catão Araujo on 06/02/2018.
 */
public abstract class StringFormatter {

    protected Integer limit;

    protected boolean justify;

    public StringFormatter(int limit, boolean justify) {
        this.limit = limit;
        this.justify = justify;
    }

    /**
     * It receives a text and should return it formatted
     *
     * @param text
     * @return
     */
    public abstract String format(String text);
}
