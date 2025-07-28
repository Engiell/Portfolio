import java.util.*;

public class ContactService {
    private final Map<String, Contact> contacts = new HashMap<>();
    private final Trie trie = new Trie();

    public void addContact(Contact contact) {
        if (contacts.containsKey(contact.getId())) {
            throw new IllegalArgumentException("Contact with this ID already exists");
        }
        contacts.put(contact.getId(), contact);
        trie.insert(contact.getFirstName(), contact);  // Insert into Trie for name-based search
    }

    public void deleteContact(String id) {
        Contact contact = contacts.get(id);
        if (contact != null) {
            trie.remove(contact.getFirstName(), contact);  // Optional: Remove from Trie
        }
        contacts.remove(id);
    }

    public void updateContact(String id, String firstName, String lastName, String phone, String address) {
        Contact contact = contacts.get(id);
        if (contact != null) {
            // If first name changes, update Trie reference
            if (!contact.getFirstName().equals(firstName)) {
                trie.remove(contact.getFirstName(), contact);
                contact.setFirstName(firstName);
                trie.insert(firstName, contact);
            }
            contact.setLastName(lastName);
            contact.setPhone(phone);
            contact.setAddress(address);
        }
    }

    // New method: Search contacts by first name prefix
    public List<Contact> searchContactsByPrefix(String prefix) {
        return trie.search(prefix);
    }
}
