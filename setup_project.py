#!/usr/bin/env python3
"""
GitHub Setup Script for Technical Drawing Analyzer
Krijon të gjithë skedarët automatikisht për upload në GitHub
"""

import os
import subprocess
import sys
from pathlib import Path

def create_all_files():
    """Krijon të gjithë skedarët e projektit"""
    
    print("🚀 Creating Technical Drawing Analyzer project files...")
    
    # Krijoni strukturën e dosjes
    os.makedirs('modules', exist_ok=True)
    
    # 1. main.py
    main_py_content = '''#!/usr/bin/env python3
"""
Technical Drawing Analyzer
Sistem i pavarur për analizë të vizatimeve teknike
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
from pathlib import Path
import json
import cv2
import numpy as np
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime

# Import modulet tona
try:
    from modules.document_processor import DocumentProcessor
    from modules.symbol_recognizer import SymbolRecognizer
    from modules.output_generator import OutputGenerator
    from modules.database_manager import DatabaseManager
except ImportError:
    print("Modulet nuk janë gjetur, duke përdorur implementim bazë...")

class TechnicalAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Technical Drawing Analyzer v1.0")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Inicializimi i komponentëve
        self.setup_database()
        self.init_processors()
        self.create_widgets()
        self.setup_styles()
        
        # Variables
        self.current_file = None
        self.analysis_results = None
        self.processed_image = None
        
    def setup_database(self):
        """Krijon bazën e të dhënave lokale"""
        try:
            self.db_manager = DatabaseManager()
            self.db_manager.initialize_database()
        except Exception as e:
            print(f"Database initialization error: {e}")
            self.db_manager = None
    
    def init_processors(self):
        """Inicializon procesorët e sistemit"""
        try:
            self.doc_processor = DocumentProcessor()
            self.symbol_recognizer = SymbolRecognizer()
            self.output_generator = OutputGenerator()
        except Exception as e:
            print(f"Processor initialization error: {e}")
            # Fallback implementations
            self.doc_processor = MockDocumentProcessor()
            self.symbol_recognizer = MockSymbolRecognizer()
            self.output_generator = MockOutputGenerator()
    
    def create_widgets(self):
        """Krijon interface-in e përdoruesit"""
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Toolbar
        self.create_toolbar(main_frame)
        
        # Main content area
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Left panel - File browser and controls
        left_panel = ttk.LabelFrame(content_frame, text="Kontrollet", padding=10)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # File selection
        ttk.Label(left_panel, text="Zgjidhni skedarin:").pack(anchor=tk.W)
        
        file_frame = ttk.Frame(left_panel)
        file_frame.pack(fill=tk.X, pady=5)
        
        self.file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_var, state="readonly", width=40).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="Browse", command=self.browse_file).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Process button
        self.process_btn = ttk.Button(left_panel, text="Proceso Dokumentin", 
                                    command=self.process_document, state=tk.DISABLED)
        self.process_btn.pack(fill=tk.X, pady=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(left_panel, variable=self.progress_var, 
                                          maximum=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Status label
        self.status_var = tk.StringVar(value="Gati për procesim...")
        ttk.Label(left_panel, textvariable=self.status_var, wraplength=200).pack(pady=5)
        
        # Analysis options
        options_frame = ttk.LabelFrame(left_panel, text="Opsionet e Analizës", padding=10)
        options_frame.pack(fill=tk.X, pady=10)
        
        self.detect_symbols = tk.BooleanVar(value=True)
        self.extract_text = tk.BooleanVar(value=True)
        self.generate_bom = tk.BooleanVar(value=True)
        self.calculate_dimensions = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(options_frame, text="Zbulo Simbolet", variable=self.detect_symbols).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Ekstrakto Tekstin", variable=self.extract_text).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Gjeneroj BOM", variable=self.generate_bom).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Kalkulo Dimensionet", variable=self.calculate_dimensions).pack(anchor=tk.W)
        
        # Export options
        export_frame = ttk.LabelFrame(left_panel, text="Eksporto Rezultatet", padding=10)
        export_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(export_frame, text="Eksporto si Excel", command=self.export_excel).pack(fill=tk.X, pady=2)
        ttk.Button(export_frame, text="Eksporto si PDF", command=self.export_pdf).pack(fill=tk.X, pady=2)
        ttk.Button(export_frame, text="Ruaj JSON", command=self.export_json).pack(fill=tk.X, pady=2)
        
        # Right panel - Display area
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Image display tab
        self.image_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.image_frame, text="Imazhi")
        
        # Canvas for image display
        canvas_frame = ttk.Frame(self.image_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white")
        h_scroll = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scroll = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Results tab
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="Rezultatet")
        
        # Results tree
        self.results_tree = ttk.Treeview(self.results_frame, columns=("Type", "Value", "Confidence"), show="tree headings")
        self.results_tree.heading("#0", text="Elementi")
        self.results_tree.heading("Type", text="Lloji")
        self.results_tree.heading("Value", text="Vlera")
        self.results_tree.heading("Confidence", text="Siguria %")
        
        results_scroll = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=results_scroll.set)
        
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        results_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # BOM tab
        self.bom_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.bom_frame, text="Bill of Materials")
        
        self.bom_tree = ttk.Treeview(self.bom_frame, columns=("Quantity", "Description", "Size", "Material", "Cost"), show="tree headings")
        self.bom_tree.heading("#0", text="Item")
        self.bom_tree.heading("Quantity", text="Sasia")
        self.bom_tree.heading("Description", text="Përshkrimi")
        self.bom_tree.heading("Size", text="Madhësia")
        self.bom_tree.heading("Material", text="Materiali")
        self.bom_tree.heading("Cost", text="Kostoja")
        
        bom_scroll = ttk.Scrollbar(self.bom_frame, orient=tk.VERTICAL, command=self.bom_tree.yview)
        self.bom_tree.configure(yscrollcommand=bom_scroll.set)
        
        self.bom_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        bom_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
    
    def create_toolbar(self, parent):
        """Krijon toolbar-in"""
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(toolbar, text="Skedar i Ri", command=self.new_project).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Hap Projektin", command=self.open_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Ruaj Projektin", command=self.save_project).pack(side=tk.LEFT, padx=5)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        ttk.Button(toolbar, text="Cilësimet", command=self.show_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Ndihmë", command=self.show_help).pack(side=tk.LEFT, padx=5)
        
        # Version info
        ttk.Label(toolbar, text="v1.0", font=("Arial", 8)).pack(side=tk.RIGHT)
    
    def setup_styles(self):
        """Vendos stilet e interface-it"""
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except:
            pass  # Use default theme if clam not available
    
    def browse_file(self):
        """Zgjedh skedarin për procesim"""
        filetypes = [
            ("Të gjitha të mbështeturit", "*.pdf *.dwg *.dxf *.png *.jpg *.jpeg *.tiff *.bmp"),
            ("PDF files", "*.pdf"),
            ("AutoCAD files", "*.dwg *.dxf"),
            ("Image files", "*.png *.jpg *.jpeg *.tiff *.bmp"),
            ("Të gjitha skedarët", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Zgjidhni dokumentin teknik",
            filetypes=filetypes
        )
        
        if filename:
            self.file_var.set(filename)
            self.current_file = filename
            self.process_btn.config(state=tk.NORMAL)
            self.load_preview()
    
    def load_preview(self):
        """Ngarkon preview të skedarit"""
        if not self.current_file:
            return
        
        try:
            self.status_var.set("Duke ngarkuar preview...")
            
            file_ext = Path(self.current_file).suffix.lower()
            
            if file_ext == '.pdf':
                image = self.doc_processor.pdf_to_image(self.current_file, page=0)
            else:
                image = cv2.imread(self.current_file)
                if image is not None:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                else:
                    raise ValueError("Could not load image")
            
            display_image = self.resize_for_display(image)
            pil_image = Image.fromarray(display_image)
            self.photo = ImageTk.PhotoImage(pil_image)
            
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
            
            self.status_var.set("Preview i ngarkuar. Gati për procesim.")
            
        except Exception as e:
            messagebox.showerror("Gabim", f"Nuk mund të ngarkojë preview: {str(e)}")
            self.status_var.set("Gabim në ngarkimin e preview")
    
    def resize_for_display(self, image, max_size=800):
        """Ridimensionon imazhin për display"""
        h, w = image.shape[:2]
        if max(h, w) > max_size:
            if h > w:
                new_h = max_size
                new_w = int(w * max_size / h)
            else:
                new_w = max_size
                new_h = int(h * max_size / w)
            image = cv2.resize(image, (new_w, new_h))
        return image
    
    def process_document(self):
        """Proceson dokumentin në background thread"""
        if not self.current_file:
            return
        
        self.process_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        
        thread = threading.Thread(target=self._process_worker)
        thread.daemon = True
        thread.start()
    
    def _process_worker(self):
        """Worker thread për procesimin"""
        try:
            self.update_status("Duke filluar procesimin...")
            self.update_progress(10)
            
            processed_data = self.doc_processor.process_file(self.current_file)
            self.update_progress(30)
            
            if self.detect_symbols.get():
                self.update_status("Duke zbuluár simbolet...")
                symbols = self.symbol_recognizer.detect_symbols(processed_data)
                self.update_progress(50)
            else:
                symbols = []
            
            if self.extract_text.get():
                self.update_status("Duke ekstraktuar tekstin...")
                text_data = self.symbol_recognizer.extract_text(processed_data)
                self.update_progress(70)
            else:
                text_data = []
            
            if self.generate_bom.get():
                self.update_status("Duke gjeneruar BOM...")
                bom_data = self.output_generator.generate_bom(symbols, text_data)
                self.update_progress(90)
            else:
                bom_data = []
            
            self.analysis_results = {
                'symbols': symbols,
                'text': text_data,
                'bom': bom_data,
                'file': self.current_file,
                'timestamp': datetime.now().isoformat()
            }
            
            self.update_progress(100)
            self.update_status("Procesimi përfundoi me sukses!")
            
            self.root.after(0, self.display_results)
            
        except Exception as e:
            self.root.after(0, lambda: self.handle_error(f"Gabim në procesim: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.process_btn.config(state=tk.NORMAL))
    
    def update_status(self, message):
        """Përditëson status në main thread"""
        self.root.after(0, lambda: self.status_var.set(message))
    
    def update_progress(self, value):
        """Përditëson progress bar në main thread"""
        self.root.after(0, lambda: self.progress_var.set(value))
    
    def handle_error(self, message):
        """Trajton gabimet"""
        messagebox.showerror("Gabim", message)
        self.status_var.set("Gabim në procesim")
        self.progress_var.set(0)
    
    def display_results(self):
        """Shfaq rezultatet në interface"""
        if not self.analysis_results:
            return
        
        self.results_tree.delete(*self.results_tree.get_children())
        self.bom_tree.delete(*self.bom_tree.get_children())
        
        if self.analysis_results.get('symbols'):
            symbols_node = self.results_tree.insert("", "end", text="Simbolet e Zbuluara")
            for i, symbol in enumerate(self.analysis_results['symbols']):
                self.results_tree.insert(symbols_node, "end", 
                                       text=f"Simboli {i+1}",
                                       values=(symbol.get('type', 'N/A'), 
                                             symbol.get('name', 'N/A'),
                                             f"{symbol.get('confidence', 0):.1f}%"))
        
        if self.analysis_results.get('text'):
            text_node = self.results_tree.insert("", "end", text="Teksti i Ekstraktuar")
            for i, text in enumerate(self.analysis_results['text']):
                self.results_tree.insert(text_node, "end",
                                       text=f"Tekst {i+1}",
                                       values=("Text", text.get('content', 'N/A'),
                                             f"{text.get('confidence', 0):.1f}%"))
        
        if self.analysis_results.get('bom'):
            for i, item in enumerate(self.analysis_results['bom']):
                self.bom_tree.insert("", "end",
                                   text=f"Item {i+1}",
                                   values=(item.get('quantity', 1),
                                         item.get('description', 'N/A'),
                                         item.get('size', 'N/A'),
                                         item.get('material', 'N/A'),
                                         item.get('cost', 'N/A')))
        
        self.notebook.select(1)
    
    # Menu functions
    def new_project(self):
        """Projekti i ri"""
        result = messagebox.askyesno("Projekti i Ri", "A dëshironi të krijoni një projekt të ri?")
        if result:
            self.current_file = None
            self.analysis_results = None
            self.file_var.set("")
            self.canvas.delete("all")
            self.results_tree.delete(*self.results_tree.get_children())
            self.bom_tree.delete(*self.bom_tree.get_children())
            self.status_var.set("Projekti i ri krijuar. Zgjidhni një skedar.")
            self.process_btn.config(state=tk.DISABLED)
    
    def open_project(self):
        """Hap projekt të ruajtur"""
        filename = filedialog.askopenfilename(
            title="Hap Projektin",
            filetypes=[("JSON files", "*.json"), ("Të gjitha skedarët", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    project_data = json.load(f)
                
                self.analysis_results = project_data
                self.current_file = project_data.get('file', '')
                self.file_var.set(self.current_file)
                
                if self.current_file and os.path.exists(self.current_file):
                    self.load_preview()
                    self.process_btn.config(state=tk.NORMAL)
                
                self.display_results()
                messagebox.showinfo("Sukses", "Projekti u hap me sukses!")
                
            except Exception as e:
                messagebox.showerror("Gabim", f"Nuk mund të hapë projektin: {str(e)}")
    
    def save_project(self):
        """Ruaj projektin"""
        if not self.analysis_results:
            messagebox.showwarning("Paralajmërim", "Nuk ka rezultate për të ruajtur!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Ruaj Projektin",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Të gjitha skedarët", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.analysis_results, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Sukses", "Projekti u ruajt me sukses!")
            except Exception as e:
                messagebox.showerror("Gabim", f"Nuk mund të ruajë projektin: {str(e)}")
    
    def export_excel(self):
        """Eksporton në Excel"""
        if not self.analysis_results:
            messagebox.showwarning("Paralajmërim", "Nuk ka rezultate për eksport!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Eksporto si Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("Të gjitha skedarët", "*.*")]
        )
        
        if filename:
            try:
                self.output_generator.export_to_excel(self.analysis_results, filename)
                messagebox.showinfo("Sukses", "Eksporti në Excel u krye me sukses!")
            except Exception as e:
                messagebox.showerror("Gabim", f"Gabim në eksport: {str(e)}")
    
    def export_pdf(self):
        """Eksporton në PDF"""
        if not self.analysis_results:
            messagebox.showwarning("Paralajmërim", "Nuk ka rezultate për eksport!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Eksporto si PDF",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("Të gjitha skedarët", "*.*")]
        )
        
        if filename:
            try:
                self.output_generator.export_to_pdf(self.analysis_results, filename)
                messagebox.showinfo("Sukses", "Eksporti në PDF u krye me sukses!")
            except Exception as e:
                messagebox.showerror("Gabim", f"Gabim në eksport: {str(e)}")
    
    def export_json(self):
        """Ruaj si JSON"""
        self.save_project()
    
    def show_settings(self):
        """Shfaq cilësimet"""
        SettingsWindow(self.root)
    
    def show_help(self):
        """Shfaq ndihmën"""
        HelpWindow(self.root)


# Mock classes për testim
class MockDocumentProcessor:
    def process_file(self, filepath):
        return {"processed": True, "file": filepath}
    
    def pdf_to_image(self, filepath, page=0):
        return np.ones((400, 600, 3), dtype=np.uint8) * 255

class MockSymbolRecognizer:
    def detect_symbols(self, data):
        return [
            {"type": "valve", "name": "Gate Valve", "confidence": 95.5, "position": [100, 200]},
            {"type": "pipe", "name": "Pipe Segment", "confidence": 89.2, "position": [300, 150]},
            {"type": "instrument", "name": "Pressure Gauge", "confidence": 92.1, "position": [450, 300]}
        ]
    
    def extract_text(self, data):
        return [
            {"content": "DN100", "confidence": 87.3, "position": [150, 180]},
            {"content": "PN16", "confidence": 91.7, "position": [380, 170]},
            {"content": "Test Drawing", "confidence": 94.1, "position": [300, 50]}
        ]

class MockOutputGenerator:
    def generate_bom(self, symbols, text):
        return [
            {"quantity": 2, "description": "Gate Valve DN100", "size": "DN100", "material": "Cast Iron", "cost": "150.00 EUR"},
            {"quantity": 5, "description": "Pipe Segment", "size": "DN100", "material": "Steel", "cost": "75.00 EUR"},
            {"quantity": 1, "description": "Pressure Gauge", "size": "0-16 bar", "material": "Stainless Steel", "cost": "45.00 EUR"}
        ]
    
    def export_to_excel(self, data, filename):
        import pandas as pd
        if data.get('bom'):
            df_bom = pd.DataFrame(data['bom'])
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df_bom.to_excel(writer, sheet_name='BOM', index=False)
    
    def export_to_pdf(self, data, filename):
        print(f"PDF export to {filename} completed (mock)")

class SettingsWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Cilësimet")
        self.window.geometry("400x300")
        self.window.transient(parent)
        self.window.grab_set()
        
        ttk.Label(self.window, text="Cilësimet e Sistemit", font=("Arial", 14, "bold")).pack(pady=10)
        
        ocr_frame = ttk.LabelFrame(self.window, text="OCR Settings", padding=10)
        ocr_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(ocr_frame, text="Gjuha e OCR:").pack(anchor=tk.W)
        ocr_lang = ttk.Combobox(ocr_frame, values=["eng", "alb", "eng+alb"])
        ocr_lang.set("eng")
        ocr_lang.pack(fill=tk.X, pady=5)
        
        proc_frame = ttk.LabelFrame(self.window, text="Processing Settings", padding=10)
        proc_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(proc_frame, text="Threshold për symbols:").pack(anchor=tk.W)
        threshold_scale = ttk.Scale(proc_frame, from_=0.5, to=1.0, orient=tk.HORIZONTAL)
        threshold_scale.set(0.8)
        threshold_scale.pack(fill=tk.X, pady=5)
