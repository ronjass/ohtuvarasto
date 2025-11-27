from flask import Flask, render_template, request, redirect, url_for
from varasto import Varasto

app = Flask(__name__)


class WarehouseManager:
    def __init__(self):
        self.warehouses = {}
        self.next_id = 1

    def get_next_id(self):
        current_id = self.next_id
        self.next_id += 1
        return current_id

    def add_warehouse(self, name, capacity, initial=0):
        warehouse_id = self.get_next_id()
        self.warehouses[warehouse_id] = {
            'name': name,
            'varasto': Varasto(capacity, initial),
            'stored_items': []
        }
        return warehouse_id


manager = WarehouseManager()


@app.route('/')
def index():
    return render_template('index.html', warehouses=manager.warehouses)


def parse_float(value, default=0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def handle_create_post():
    name = request.form.get('name', '').strip()
    capacity = parse_float(request.form.get('capacity', 0))
    initial = parse_float(request.form.get('initial', 0))
    if name and capacity > 0:
        manager.add_warehouse(name, capacity, initial)


@app.route('/create', methods=['GET', 'POST'])
def create_warehouse():
    if request.method == 'POST':
        handle_create_post()
        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/edit/<int:warehouse_id>', methods=['GET', 'POST'])
def edit_warehouse(warehouse_id):
    if warehouse_id not in manager.warehouses:
        return redirect(url_for('index'))

    warehouse = manager.warehouses[warehouse_id]
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            warehouse['name'] = name
        return redirect(url_for('index'))
    return render_template('edit.html', warehouse_id=warehouse_id,
                           warehouse=warehouse)


def do_add_content(warehouse_id):
    if warehouse_id not in manager.warehouses:
        return
    amount = parse_float(request.form.get('amount', 0))
    item_name = request.form.get('item_name', '').strip()
    if amount <= 0:
        return
    warehouse = manager.warehouses[warehouse_id]
    warehouse['varasto'].lisaa_varastoon(amount)
    if item_name:
        warehouse['stored_items'].append({'name': item_name, 'amount': amount})


@app.route('/add/<int:warehouse_id>', methods=['POST'])
def add_content(warehouse_id):
    if warehouse_id in manager.warehouses:
        do_add_content(warehouse_id)
    return redirect(url_for('index'))


@app.route('/remove/<int:warehouse_id>/<int:item_index>', methods=['POST'])
def remove_content(warehouse_id, item_index):
    if warehouse_id not in manager.warehouses:
        return redirect(url_for('index'))
    warehouse = manager.warehouses[warehouse_id]
    items = warehouse['stored_items']
    if 0 <= item_index < len(items):
        item = items[item_index]
        warehouse['varasto'].ota_varastosta(item['amount'])
        items.pop(item_index)
    return redirect(url_for('index'))


@app.route('/delete/<int:warehouse_id>', methods=['POST'])
def delete_warehouse(warehouse_id):
    if warehouse_id in manager.warehouses:
        del manager.warehouses[warehouse_id]
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
