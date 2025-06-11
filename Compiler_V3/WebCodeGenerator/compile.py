from Compiler_V3 import validate_and_generate_ast, linter_formatter, validate_dsl
from Compiler_V3.WebCodeGenerator.clean_and_format_html_css import clean_and_format_html_css
from Compiler_V3.WebCodeGenerator.generator import generate_html
from Compiler_V3.WebCodeGenerator.layout.wrappers import html_wrapper, css_wrapper


def compile_to_web(dslCode: str):
    is_valid, ast_tree, error_message = validate_and_generate_ast(dslCode)
    html, css = generate_html(ast_tree)
    html = html_wrapper(html)
    css = css_wrapper(css)
    formatted_html, _ = clean_and_format_html_css(html, css)

    # Write formatted HTML to file
    with open("/home/mohab/test/index.html", "w", encoding="utf-8") as html_file:
        html_file.write(formatted_html)

    # Write formatted CSS to file
    with open("/home/mohab/test/style.css", "w", encoding="utf-8") as css_file:
        css_file.write(css)

dsl = """
header<title=("Louis Viton"),args=["Home", "Shop", "Sale", "Categories", "Contact"]>
side_nav<args=["All Products", "New Arrivals", "Best Sellers", "Sale", "Brands", "Price Range"]>
row{
    box<align_items=("center")>{
     title<text=("Products")>
     }
},
row<testtag=("product-row")>{
    box<align_items=("center")>{
        image<src=("https://us.louisvuitton.com/images/is/image/lv/1/PP_VP_L/louis-vuitton-lv-trainer-sneaker-distressed--BS9U1PWA22_PM2_Front%20view.png?wid=1090&hei=1090")>,
        title<text=("LV Sneaker")>,
        text<text=("1.300.00$")>
    },
    box<align_items=("center")>{
        image<src=("https://us.louisvuitton.com/images/is/image/lv/1/PP_VP_L/louis-vuitton-printed-monogram-windbreaker--HTB08WVKX619_PM2_Front%20view.png?wid=2400&hei=2400")>,
        title<text=("Windbreaker")>,
        text<text=("3.200.00$")>
    },
    box<align_items=("center")>{
        image<src=("https://us.louisvuitton.com/images/is/image/lv/1/PP_VP_L/louis-vuitton-jacquard-denim-shorts--HRD25XLJG650_PM2_Front%20view.png?wid=1090&hei=1090")>,
        title<text=("Denim Shorts")>,
        text<text=("1,890.00$")>
    }
},
row<testtag=("product-row")>{
    box<align_items=("center")>{
        image<src=("https://us.louisvuitton.com/images/is/image/lv/1/PP_VP_L/louis-vuitton-signature-cap--M5148M_PM2_Front%20view.png?wid=1090&hei=1090")>,
        title<text=("Cap")>,
        text<text=("545.00$")>
    },
    box<align_items=("center")>{
        image<src=("https://us.louisvuitton.com/images/is/image/lv/1/PP_VP_L/louis-vuitton-lv-venice-mule--BTHI2SGC02_PM2_Front%20view.png?wid=1090&hei=1090")>,
        title<text=("Venice")>,
        text<text=("925.00$")>
    },
    box<align_items=("center")>{
        image<src=("https://us.louisvuitton.com/images/is/image/lv/1/PP_VP_L/louis-vuitton-wallet-on-chain-ivy--M82154_PM2_Front%20view.png?wid=1090&hei=1090")>,
        title<text=("Wallet")>,
        text<text=("1,990.00$")>
    }
}
footer<title=("LV"),args=["Privacy Policy", "Terms of Service", "Contact Us"]>
"""
print(validate_dsl(dsl))
compile_to_web(dsl)
print(linter_formatter(dsl))
