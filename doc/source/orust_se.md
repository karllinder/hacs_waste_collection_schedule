# Orust Avfall och återvinning

This is a waste collection schedule integration for the Orust. 

## Configuration via configuration.yaml

```yaml
waste_collection_schedule:
  sources:
    - name: orust_se
      args:
        street_address: STREET_ADDRESS
```

### Configuration Variables

**street_address**  
*(string) (required)*

## Example

```yaml
waste_collection_schedule:
  sources:
    - name: orust_se
      args:
        street_address: Åvägen 2, Henån
```

## How to get the source argument

The source argument is the address to the house with waste collection, this can be seen on the "mina sidor" or search in the setup.
