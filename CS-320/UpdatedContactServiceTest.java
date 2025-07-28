import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.List;

public class ContactServiceTest {

    @Test
    public void testAddAndSearchContactsByPrefix() {
        ContactService service = new ContactService();

        Contact a = new Contact("1", "Mike", "Smith", "1234567890", "123 Widow Street");
        Contact b = new Contact("2", "Melissa", "Brown", "2345678901", "456 Fell Avenue");
        Contact c = new Contact("3", "Rachel", "Smith", "3456789012", "789 Willowwood Drive");

        service.addContact(a);
        service.addContact(b);
        service.addContact(c);

        List<Contact> results = service.searchContactsByPrefix("An");

        assertEquals(2, results.size());
        assertTrue(results.contains(a));
        assertTrue(results.contains(b));
        assertFalse(results.contains(c));
    }

    @Test
    public void testUpdateContactFirstNameAndSearch() {
        ContactService service = new ContactService();

        Contact contact = new Contact("4", "Amy", "Stone", "4567890123", "987 Cedar Lane");
        service.addContact(contact);

        // Search by old name
        assertEquals(1, service.searchContactsByPrefix("Am").size());

        // Update name and verify Trie reflects change
        service.updateContact("4", "Eve", "Stone", "4567890123", "987 Cedar Lane");
        assertEquals(0, service.searchContactsByPrefix("Am").size());
        assertEquals(1, service.searchContactsByPrefix("Ev").size());
    }
}
