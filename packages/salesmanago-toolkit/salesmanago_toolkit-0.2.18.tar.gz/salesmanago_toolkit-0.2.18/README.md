# salesmanago-tools

Python Class for SalesManago integration.

## Installation

pip install salesmanago-tools

## Third Party Libraries and Dependencies

The following libraries will be installed when you install the client library:

- requests
- aiohttp
- pandas

# Class

Start with import `from salesmanago_tools.utils import SalesmanagoDataClient`

## Initialization
```
salesmanago_client = SalesmanagoDataClient(
    clientId="YOUR CLIENT_ID",
    apiKey="YOUR API_KEY",
    sha="YOUR OWNER_EMAIL",
    owner="YOUR SHA",
)
```

## Export data with example
Initiates the export process for specific data and returns the data as a CSV generator.
- param value: The value associated with the export, such as an email or tag.
- param addresseeType: The type of recipient (default is "tag").
- return: A CSV generator containing the exported data.

```
async def example_call_export_data():
    contacts = await salesmanago_client.export_data(value="TEST_TAG", addresseeType="tag")
    return contacts


asyncio.run(example_call_export_data())
```
This function will make a request to export contacts by tag TEST_TAG

## Fetch all contacts from salesmanago

Fetches all contacts from SalesManago and returns them as a list.
- param page_size: The number of contacts to retrieve per request (default is 1000).
- param page: The page number to fetch (default is 1).
- return: A list of contacts, with each contact formatted as a list of details.


```
async def example_call_fetch_all_contacts_from_salesmanago():
    contacts = await salesmanago_client.fetch_all_contacts_from_salesmanago()
    return contacts


asyncio.run(example_call_fetch_all_contacts_from_salesmanago())
```
This function will make a request to export all contacts without any filters

## Push people to salesmanago
Pushes a list of people to Salesmanago for upsert, handling each person's details and tags.

- param people_list_to_push: A list of people data (dictionaries) ("Email", "Phone", "Country", "City", "Name", "properties") to push to Salesmanago.
- param tags: A list of tags to associate with each person (default is an empty list).
- return: None
```
async def example_call_push_people_to_salesmanago():

    await salesmanago_client.push_people_to_salesmanago(
        people_list_to_push=[
            {
                "Email": "example@gmail.com",
                "Phone": "+380000000000",
                "Country": "Ukraine",
                "City": "Dnipro",
                "Name": "Name Surname",
                "properties": {
                    "property1": 1000,
                    "property2": False,
                    "property3": "3000"

                }
            },
            {
                "Email": "example2@gmail.com",
                "Phone": "+38111111111",
                "Country": "Ukraine",
                "City": "Kharkiv",
                "Name": "Name Second Surname",
                "properties": {
                    "property1": 1000,
                    "property2": False,
                    "property3": "3000"

                }
            },
        ],
        tags=["TAG1, TAG2"]
    )


asyncio.run(example_call_push_people_to_salesmanago())
```

In this example we have added two people, each of them will have tags TAG1 and TAG2

## Update tag salesmanago

Updates the tags for a specific contact in Salesmanago.

- param email: The email of the contact whose tags are to be updated.
- param tags: A list of tags to assign to the contact.
- return: None

```
async def example_call_update_tag_salesmanago():
    await salesmanago_client.update_tag_salesmanago(
        email="example@gmail.com", 
        tags=["TAG1", "TAG2"]
    )

asyncio.run(example_call_update_tag_salesmanago())
```

In this example we have added TAG1 and TAG2 tags to person whose email is example@gmail.com

## Delete tag salesmanago

Deletes the tags for a specific contact in Salesmanago.

- param email: The email of the contact whose tags are to be deleted.
- param tags: A list of tags to delete from the contact.
- return: None

```
async def example_call_delete_tag_salesmanago():
    await salesmanago_client.delete_tag_salesmanago(
        email="example@gmail.com", 
        tags=["TAG1", "TAG2"]
    )

asyncio.run(example_call_delete_tag_salesmanago())
```

In this example we have deleted TAG1 and TAG2 tags from person whose email is example@gmail.com

## Update standard details salesmanago

Updates the standard details for a specific contact in Salesmanago.

- param email: The email of the contact whose tags are to be updated.
- param properties: A dictionary of properties to assign to the contact.
- return: None

```
async def example_call_update_standard_details_salesmanago():

    await salesmanago_client.update_standard_details_salesmanago(
        email="example@gmail.com", 
        properties={"standard1_detail": 1, "standard2_detail": "2"}
    )

asyncio.run(example_call_update_standard_details_salesmanago())
```

In this example we have added TAG1 and TAG2 tags to person whose email is example@gmail.com

## Get contact info by email

Retrieves detailed contact information by email from Salesmanago.

- param contact_email: The email of the contact to retrieve information for.
- return: A dictionary with contact details including name, company, tags, and other properties.


```
async def example_call_get_contact_info_by_email():
    contact = await salesmanago_client.get_contact_info_by_email(contact_email="example@gmail.com")
    return contact

asyncio.run(example_call_get_contact_info_by_email())
```
In this example, we got additional information about the user knowing only his email.


## Add or modify contact

Adds or modifies a contact in Salesmanago.

- param email: The email of the contact to add or modify.
- param tags: A list of tags to assign to the contact.
- param properties: A dictionary of properties to set for the contact.
- param additional_contact_info: A dictionary of additional contact information such as phone, company, etc.
- param kwargs: Additional keyword arguments for custom fields like useApiDoubleOptIn, doubleOptInEmailId, etc.

```
async def example_add_or_modify_contact():
    await salesmanago_client.add_or_modify_contact(
        email="example@gmail.com",
        tags=["test1", "test2"],
        properties={"test_property": "test_value"},
        additional_contact_info={"phone": "+1234567890", "company": "Test Company"},
        forceOptIn=True,
        forceOptOut=False,
        forcePhoneOptIn=False,
        forcePhoneOptOut=True,
        useApiDoubleOptIn=True,
        doubleOptInLanguage="ES",
    )

asyncio.run(example_add_or_modify_contact())
```

