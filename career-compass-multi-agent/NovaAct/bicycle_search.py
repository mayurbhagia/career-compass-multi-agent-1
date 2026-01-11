# bicycle_search.py
from nova_act import NovaAct, workflow

@workflow(workflow_definition_name="bicycle_search_demo", model_id="nova-act-latest")
def search_and_add_bicycle():
    """
    Demo: Search for a bicycle on Amazon.in and add to cart
    """
    with NovaAct(starting_page="https://www.amazon.in") as nova:
        # Search for bicycle
        nova.act("Search for 'bicycle' in the search box")

        # Select first result
        nova.act("Click on the first bicycle in the search results")

        # Add to cart
        nova.act("Scroll down until you see 'Add to Cart' button and click it")

        print("✅ Bicycle added to cart successfully!")

if __name__ == "__main__":
    print("🚀 Starting Amazon.in Bicycle Search Demo...")
    search_and_add_bicycle()
    print("✅ Demo Complete!")