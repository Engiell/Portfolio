import java.util.*;

public class TrieNode {
    Map<Character, TrieNode> children = new HashMap<>();
    boolean isEndOfName = false;
    List<Contact> contacts = new ArrayList<>();
}
