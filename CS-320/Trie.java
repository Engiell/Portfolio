import java.util.*;

public class Trie {
    private final TrieNode root = new TrieNode();

    public void insert(String name, Contact contact) {
        TrieNode node = root;
        for (char ch : name.toLowerCase().toCharArray()) {
            node = node.children.computeIfAbsent(ch, c -> new TrieNode());
        }
        node.isEndOfName = true;
        node.contacts.add(contact);
    }

    public void remove(String name, Contact contact) {
        TrieNode node = root;
        for (char ch : name.toLowerCase().toCharArray()) {
            node = node.children.get(ch);
            if (node == null) return;
        }
        node.contacts.remove(contact);
        // Optional: Cleanup empty nodes (not required for this milestone)
    }

    public List<Contact> search(String prefix) {
        TrieNode node = root;
        for (char ch : prefix.toLowerCase().toCharArray()) {
            node = node.children.get(ch);
            if (node == null) return Collections.emptyList();
        }
        return collectContacts(node);
    }

    private List<Contact> collectContacts(TrieNode node) {
        List<Contact> result = new ArrayList<>();
        if (node.isEndOfName) result.addAll(node.contacts);
        for (TrieNode child : node.children.values()) {
            result.addAll(collectContacts(child));
        }
        return result;
    }
}
