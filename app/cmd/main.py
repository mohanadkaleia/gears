from app.models import services

# TODO: initialize services 
pass

def create_services(shop_id=None):    
    seeds = [
        {            
            "name": "Detail",
            "description": "Get the absolute best look for your paintwork and surfaces. A clean or a valet is about making sure all surfaces are, well, clean.",
            "images": ["/static/images/detail_service.jpeg"],
        }, 
        {            
            "name": "Lube, Oil, and Filters",
            "images": ["/static/images/detail_service.jpeg"],
            "description": "An oil change and filter replacement is one of many preventative maintenance services that help promote maximum vehicle performance while extending the life of your vehicle. Oil is responsible for lubricating the working components inside your vehicle's engine while reducing the amount of friction between them."
        }, 
        {            
            "name": "Inspection",
            "images": ["/static/images/detail_service.jpeg"],
            "description": "Vehicle inspection is a procedure mandated by national or subnational governments in many countries, in which a vehicle is inspected to ensure that it conforms to regulations governing safety, emissions, or both. Inspection can be required at various times, e.g., periodically or on the transfer of title to a vehicle."
        }, 
        {            
            "name": "Tire Installation",
            "images": ["/static/images/tire_installation.jpeg"],
            "description": "Comming soon"
        },
    ]

    for service in seeds:
        try:
            services.get_by_name(service['name'])
        except services.ErrNotFound:
            services.insert(shop_id=shop_id, name=service['name'], description=service['description'])
            print(f"Service {service['name']} has been added")
        
    
def main():
    create_services(shop_id=1)

if __name__ == 'main':
    main()