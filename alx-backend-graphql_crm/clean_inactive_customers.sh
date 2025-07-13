#!/bin/bash

# Run Django shell command to delete customers inactive for 1 year

deleted_count=$(python3 manage.py shell << EOF
from crm.models import Customer, Order
from datetime import datetime, timedelta

one_year_ago = datetime.now() - timedelta(days=365)

# Find customers with no orders in past year
inactive_customers = Customer.objects.exclude(
    id__in=Order.objects.filter(order_date__gte=one_year_ago).values_list('customer_id', flat=True)
)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
EOF
)

echo "$(date '+%Y-%m-%d %H:%M:%S') - Deleted $deleted_count inactive customers" >> /tmp/customer_cleanup_log.txt
