"""
ETH Key Scanner - Android App
Main application file with Kivy UI
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform

import os
import sys
import importlib.util
import threading

# Import the scanner
from eth_key_scanner import ETHKeyScanner, PatternFilter, NoRepeatingFilter, NoTripleTripleFilter

# Set window size for development (will be full screen on Android)
if platform != 'android':
    Window.size = (400, 700)


class FilterItem(BoxLayout):
    """Widget for displaying a single filter with checkbox"""
    
    def __init__(self, filter_name, filter_obj, on_toggle, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 50
        self.padding = [10, 5]
        self.spacing = 10
        
        self.filter_obj = filter_obj
        self.filter_name = filter_name
        self.on_toggle = on_toggle
        
        # Checkbox
        self.checkbox = CheckBox(
            size_hint_x=0.15,
            active=True
        )
        self.checkbox.bind(active=self._on_checkbox)
        
        # Label
        self.label = Label(
            text=filter_name,
            size_hint_x=0.85,
            halign='left',
            valign='middle',
            text_size=(None, None)
        )
        self.label.bind(size=self._update_text_size)
        
        self.add_widget(self.checkbox)
        self.add_widget(self.label)
    
    def _update_text_size(self, instance, value):
        self.label.text_size = (self.label.width, None)
    
    def _on_checkbox(self, checkbox, value):
        self.on_toggle(self.filter_name, self.filter_obj, value)


class ETHKeyScannerApp(App):
    
    def build(self):
        self.title = "ETH Key Scanner"
        
        # Initialize scanner with default filters
        self.default_filters = {
            'NoRepeating(6)': NoRepeatingFilter(max_repeats=6),
            'NoTripleTriple': NoTripleTripleFilter()
        }
        
        self.custom_filters = {}
        self.active_filters = self.default_filters.copy()
        
        self.scanner = ETHKeyScanner(filters=list(self.active_filters.values()))
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='ETH Key Scanner',
            size_hint_y=None,
            height=50,
            font_size='24sp',
            bold=True
        )
        main_layout.add_widget(title)
        
        # Filters section
        filters_label = Label(
            text='Active Filters:',
            size_hint_y=None,
            height=30,
            font_size='18sp',
            bold=True
        )
        main_layout.add_widget(filters_label)
        
        # Filters scrollview
        self.filters_layout = GridLayout(
            cols=1,
            spacing=5,
            size_hint_y=None
        )
        self.filters_layout.bind(minimum_height=self.filters_layout.setter('height'))
        
        filters_scroll = ScrollView(size_hint=(1, 0.25))
        filters_scroll.add_widget(self.filters_layout)
        main_layout.add_widget(filters_scroll)
        
        # Load filters button
        load_filter_btn = Button(
            text='Load Custom Filter (.py)',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 1, 1)
        )
        load_filter_btn.bind(on_press=self.open_file_chooser)
        main_layout.add_widget(load_filter_btn)
        
        # Batch size input
        batch_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        batch_layout.add_widget(Label(text='Batch Size:', size_hint_x=0.4))
        self.batch_input = TextInput(
            text='10',
            multiline=False,
            input_filter='int',
            size_hint_x=0.6
        )
        batch_layout.add_widget(self.batch_input)
        main_layout.add_widget(batch_layout)
        
        # API Key input
        api_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        api_layout.add_widget(Label(text='Etherscan API:', size_hint_x=0.4, font_size='12sp'))
        self.api_input = TextInput(
            text='',
            hint_text='Optional',
            multiline=False,
            size_hint_x=0.6
        )
        api_layout.add_widget(self.api_input)
        main_layout.add_widget(api_layout)
        
        # Check balance checkbox
        balance_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        balance_layout.add_widget(Label(text='Check Balances:', size_hint_x=0.6))
        self.check_balance = CheckBox(active=True, size_hint_x=0.4)
        balance_layout.add_widget(self.check_balance)
        main_layout.add_widget(balance_layout)
        
        # Generate button
        self.generate_btn = Button(
            text='Generate Keys',
            size_hint_y=None,
            height=60,
            background_color=(0.2, 0.8, 0.2, 1),
            font_size='18sp',
            bold=True
        )
        self.generate_btn.bind(on_press=self.generate_keys)
        main_layout.add_widget(self.generate_btn)
        
        # Results/Log area
        results_label = Label(
            text='Results:',
            size_hint_y=None,
            height=30,
            font_size='16sp',
            bold=True
        )
        main_layout.add_widget(results_label)
        
        self.results_text = TextInput(
            text='Ready to generate keys...\n',
            multiline=True,
            readonly=True,
            size_hint=(1, 0.3)
        )
        main_layout.add_widget(self.results_text)
        
        # Populate filters
        self.refresh_filters()
        
        return main_layout
    
    def refresh_filters(self):
        """Refresh the filters display"""
        self.filters_layout.clear_widgets()
        
        all_filters = {**self.default_filters, **self.custom_filters}
        
        for name, filter_obj in all_filters.items():
            is_active = name in self.active_filters
            filter_item = FilterItem(name, filter_obj, self.on_filter_toggle)
            filter_item.checkbox.active = is_active
            self.filters_layout.add_widget(filter_item)
    
    def on_filter_toggle(self, filter_name, filter_obj, is_active):
        """Handle filter checkbox toggle"""
        if is_active:
            self.active_filters[filter_name] = filter_obj
        else:
            if filter_name in self.active_filters:
                del self.active_filters[filter_name]
        
        # Update scanner
        self.scanner = ETHKeyScanner(filters=list(self.active_filters.values()))
        self.log(f"Filter '{filter_name}' {'enabled' if is_active else 'disabled'}")
    
    def open_file_chooser(self, instance):
        """Open file chooser to load custom filter"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # File chooser
        if platform == 'android':
            # On Android, start in external storage
            from android.storage import primary_external_storage_path
            initial_path = primary_external_storage_path()
        else:
            initial_path = os.path.expanduser('~')
        
        filechooser = FileChooserListView(
            path=initial_path,
            filters=['*.py']
        )
        content.add_widget(filechooser)
        
        # Buttons
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        load_btn = Button(text='Load', background_color=(0.2, 0.8, 0.2, 1))
        cancel_btn = Button(text='Cancel', background_color=(0.8, 0.2, 0.2, 1))
        
        btn_layout.add_widget(load_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Select Filter File',
            content=content,
            size_hint=(0.9, 0.9)
        )
        
        def load_file(instance):
            if filechooser.selection:
                self.load_custom_filter(filechooser.selection[0])
            popup.dismiss()
        
        load_btn.bind(on_press=load_file)
        cancel_btn.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def load_custom_filter(self, filepath):
        """Load a custom filter from a Python file"""
        try:
            # Import the module
            spec = importlib.util.spec_from_file_location("custom_filter", filepath)
            module = importlib.util.module_from_spec(spec)
            sys.modules["custom_filter"] = module
            spec.loader.exec_module(module)
            
            # Find PatternFilter subclasses
            from eth_key_scanner import PatternFilter
            
            loaded_count = 0
            for name in dir(module):
                obj = getattr(module, name)
                if (isinstance(obj, type) and 
                    issubclass(obj, PatternFilter) and 
                    obj is not PatternFilter):
                    try:
                        # Try to instantiate with no args
                        filter_instance = obj()
                        filter_name = filter_instance.get_name()
                        
                        if filter_name not in self.custom_filters:
                            self.custom_filters[filter_name] = filter_instance
                            self.active_filters[filter_name] = filter_instance
                            loaded_count += 1
                    except:
                        self.log(f"Could not instantiate {name} (may need parameters)")
            
            if loaded_count > 0:
                self.refresh_filters()
                self.log(f"Loaded {loaded_count} filter(s) from {os.path.basename(filepath)}")
            else:
                self.log(f"No compatible filters found in {os.path.basename(filepath)}")
                
        except Exception as e:
            self.log(f"Error loading filter: {str(e)}")
    
    def log(self, message):
        """Add message to results text"""
        self.results_text.text += f"{message}\n"
        # Scroll to bottom
        self.results_text.cursor = (0, 0)
    
    def generate_keys(self, instance):
        """Generate keys in background thread"""
        try:
            batch_size = int(self.batch_input.text)
            if batch_size < 1 or batch_size > 1000:
                self.log("Batch size must be between 1 and 1000")
                return
        except:
            self.log("Invalid batch size")
            return
        
        # Disable button
        self.generate_btn.disabled = True
        self.generate_btn.text = "Generating..."
        
        # Clear results
        self.results_text.text = ""
        
        # Run in thread
        thread = threading.Thread(
            target=self._generate_keys_thread,
            args=(batch_size,)
        )
        thread.daemon = True
        thread.start()
    
    def _generate_keys_thread(self, batch_size):
        """Background thread for key generation"""
        try:
            api_key = self.api_input.text.strip() or None
            check_balances = self.check_balance.active
            
            Clock.schedule_once(lambda dt: self.log(f"Generating {batch_size} keys..."))
            Clock.schedule_once(lambda dt: self.log(f"Active filters: {len(self.active_filters)}"))
            
            results = self.scanner.generate_and_check_batch(
                batch_size=batch_size,
                check_balances=check_balances,
                api_key=api_key,
                delay=0.2
            )
            
            # Display results
            Clock.schedule_once(lambda dt: self.log("\n=== RESULTS ==="))
            
            for i, result in enumerate(results, 1):
                msg = f"\n#{i}\n"
                msg += f"Key: {result['private_key'][:16]}...\n"
                msg += f"Addr: {result['address'][:20]}...\n"
                
                if result['balance'] is not None:
                    msg += f"Balance: {result['balance']} ETH\n"
                    
                    if result['balance'] > 0:
                        msg = f"🎯 BALANCE FOUND!\n{msg}"
                
                Clock.schedule_once(lambda dt, m=msg: self.log(m))
            
            # Stats
            stats = self.scanner.stats
            Clock.schedule_once(lambda dt: self.log("\n=== STATS ==="))
            Clock.schedule_once(lambda dt: self.log(f"Generated: {stats['generated']}"))
            Clock.schedule_once(lambda dt: self.log(f"Filtered: {stats['filtered']}"))
            Clock.schedule_once(lambda dt: self.log(f"Checked: {stats['checked']}"))
            Clock.schedule_once(lambda dt: self.log(f"With balance: {stats['with_balance']}"))
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.log(f"Error: {str(e)}"))
        
        finally:
            # Re-enable button
            Clock.schedule_once(lambda dt: setattr(self.generate_btn, 'disabled', False))
            Clock.schedule_once(lambda dt: setattr(self.generate_btn, 'text', 'Generate Keys'))


if __name__ == '__main__':
    ETHKeyScannerApp().run()
