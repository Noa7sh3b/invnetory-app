"""
Sales Analysis Page - Advanced sales performance analytics and reporting.

Provides detailed analysis of product sales, profit margins, trends,
and customer performance with interactive charts and PDF export capability.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from services.sales_analysis_service import (
    get_sales_analysis_summary,
    get_product_sales_summary,
    get_category_sales_performance,
    get_profit_margin_by_product,
    get_customer_sales_ranking,
    get_sales_trend_by_month
)
from ui.components import render_metric_cards
from datetime import datetime


def format_currency(value):
    """Format number as currency"""
    return f"${value:,.2f}"


def format_number(value):
    """Format number with thousand separators"""
    return f"{int(value):,}"


def render_top_bottom_products(summary):
    """Render top and bottom selling products cards"""
    st.markdown("### 🏆 Best & Worst Performing Products")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if summary["top_product"]:
            product_id, name, qty_sold, revenue, profit = summary["top_product"]
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 25px; border-radius: 15px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
                <div style='font-size: 14px; opacity: 0.9; margin-bottom: 5px;'>🥇 TOP SELLING PRODUCT</div>
                <div style='font-size: 24px; font-weight: bold; margin-bottom: 10px;'>{name}</div>
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;'>
                    <div>
                        <div style='font-size: 12px; opacity: 0.8;'>Units Sold</div>
                        <div style='font-size: 22px; font-weight: bold;'>{format_number(qty_sold)}</div>
                    </div>
                    <div>
                        <div style='font-size: 12px; opacity: 0.8;'>Total Profit</div>
                        <div style='font-size: 22px; font-weight: bold; color: #90EE90;'>{format_currency(profit)}</div>
                    </div>
                </div>
                <div style='margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.2);'>
                    <div style='font-size: 12px; opacity: 0.8;'>Total Revenue</div>
                    <div style='font-size: 18px; font-weight: bold;'>{format_currency(revenue)}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No sales data available")
    
    with col2:
        if summary["bottom_product"]:
            product_id, name, qty_sold, revenue, profit = summary["bottom_product"]
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 25px; border-radius: 15px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
                <div style='font-size: 14px; opacity: 0.9; margin-bottom: 5px;'>📉 LOWEST SELLING PRODUCT</div>
                <div style='font-size: 24px; font-weight: bold; margin-bottom: 10px;'>{name}</div>
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;'>
                    <div>
                        <div style='font-size: 12px; opacity: 0.8;'>Units Sold</div>
                        <div style='font-size: 22px; font-weight: bold;'>{format_number(qty_sold)}</div>
                    </div>
                    <div>
                        <div style='font-size: 12px; opacity: 0.8;'>Total Profit</div>
                        <div style='font-size: 22px; font-weight: bold; color: #FFD700;'>{format_currency(profit)}</div>
                    </div>
                </div>
                <div style='margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.2);'>
                    <div style='font-size: 12px; opacity: 0.8;'>Total Revenue</div>
                    <div style='font-size: 18px; font-weight: bold;'>{format_currency(revenue)}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No sales data available")


def render_top_products_chart(top_products):
    """Render bar chart for top selling products"""
    if not top_products:
        st.info("No product sales data available for chart")
        return
    
    # Prepare data
    df = pd.DataFrame(top_products, columns=[
        "product_id", "product_name", "sku", "quantity_sold", 
        "revenue", "avg_price", "cost", "profit", "num_sales"
    ])
    
    # Create figure with secondary y-axis
    fig = go.Figure()
    
    # Add bars for quantity sold
    fig.add_trace(go.Bar(
        x=df["product_name"],
        y=df["quantity_sold"],
        name="Units Sold",
        marker_color='#4ECDC4',
        text=df["quantity_sold"].apply(lambda x: f"{int(x):,}"),
        textposition='outside',
        yaxis='y',
        hovertemplate='<b>%{x}</b><br>Units Sold: %{y:,}<extra></extra>'
    ))
    
    # Add bars for profit
    fig.add_trace(go.Bar(
        x=df["product_name"],
        y=df["profit"],
        name="Profit",
        marker_color='#95E1D3',
        text=df["profit"].apply(lambda x: f"${x:,.0f}"),
        textposition='outside',
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>Profit: $%{y:,.2f}<extra></extra>'
    ))
    
    # Update layout
    fig.update_layout(
        title={
            'text': "📊 Top Products Performance Analysis",
            'font': {'size': 24, 'color': '#2C3E50', 'family': 'Arial Black'}
        },
        xaxis=dict(
            title="Product Name",
            tickangle=-45,
            tickfont=dict(size=11),
            showspikes=False
        ),
        yaxis=dict(
            title=dict(text="Units Sold", font=dict(color="#4ECDC4")),
            tickfont=dict(color="#4ECDC4"),
            side='left',
            showspikes=False
        ),
        yaxis2=dict(
            title=dict(text="Profit ($)", font=dict(color="#95E1D3")),
            tickfont=dict(color="#95E1D3"),
            overlaying='y',
            side='right',
            showspikes=False
        ),
        height=550,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif"),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        barmode='group',
        transition_duration=0
    )
    
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': False,
        'staticPlot': True,
        'displaylogo': False
    })


def render_profit_margin_chart(products):
    """Render profit margin comparison chart"""
    if not products:
        st.info("No profit margin data available")
        return
    
    df = pd.DataFrame(products, columns=[
        "product_id", "product_name", "revenue", "cost", "profit", "profit_margin"
    ])
    
    # Create horizontal bar chart for profit margins
    fig = px.bar(
        df,
        x="profit_margin",
        y="product_name",
        orientation='h',
        title="💰 Profit Margin by Product (%)",
        labels={"profit_margin": "Profit Margin (%)", "product_name": "Product"},
        text=df["profit_margin"].apply(lambda x: f"{x:.1f}%"),
        color="profit_margin",
        color_continuous_scale=["#FF6B6B", "#FFD93D", "#6BCB77"],
    )
    
    fig.update_traces(textposition='outside')
    fig.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_size=20,
        title_font_color='#2C3E50',
        font=dict(family="Arial, sans-serif"),
        transition_duration=0
    )
    
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': False,
        'staticPlot': True,
        'displaylogo': False
    })


def render_category_performance(categories):
    """Render category sales performance pie chart"""
    if not categories:
        st.info("No category data available")
        return
    
    df = pd.DataFrame(categories, columns=[
        "category_name", "products_count", "quantity_sold", "revenue", "profit"
    ])
    
    # Create donut chart
    fig = px.pie(
        df,
        values="revenue",
        names="category_name",
        title="📦 Revenue Distribution by Category",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(
        textposition='outside',
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Revenue: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        height=400,
        title_font_size=20,
        title_font_color='#2C3E50',
        font=dict(family="Arial, sans-serif", size=12),
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.1),
        transition_duration=0
    )
    
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': False,
        'staticPlot': True,
        'displaylogo': False
    })


def render_sales_trend(months=6):
    """Render sales trend over time"""
    trend_data = get_sales_trend_by_month(months)
    
    if not trend_data:
        st.info(f"No sales trend data available for the last {months} months")
        return
    
    df = pd.DataFrame(trend_data, columns=["month", "quantity", "revenue", "profit"])
    
    # Create line chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df["month"],
        y=df["revenue"],
        name="Revenue",
        line=dict(color='#667eea', width=3),
        mode='lines+markers',
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.1)'
    ))
    
    fig.add_trace(go.Scatter(
        x=df["month"],
        y=df["profit"],
        name="Profit",
        line=dict(color='#f093fb', width=3),
        mode='lines+markers',
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(240, 147, 251, 0.1)'
    ))
    
    fig.update_layout(
        title={
            'text': f"📈 Sales Trend - Last {months} Months",
            'font': {'size': 20, 'color': '#2C3E50'}
        },
        xaxis=dict(
            title="Month",
            showspikes=False
        ),
        yaxis=dict(
            title="Amount ($)",
            showspikes=False
        ),
        height=400,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif"),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        transition_duration=0
    )
    
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': False,
        'staticPlot': True,
        'displaylogo': False
    })


def export_to_pdf():
    """Generate and download PDF report of sales analysis"""
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    import io
    
    # Get data
    summary = get_sales_analysis_summary()
    top_products = get_product_sales_summary(limit=10)
    
    # Create PDF buffer
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495E'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    # Title
    story.append(Paragraph("Sales Analysis Report", title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Overall Statistics
    story.append(Paragraph("Overall Performance", heading_style))
    stats = summary["overall_stats"]
    stats_data = [
        ["Metric", "Value"],
        ["Total Invoices", format_number(stats["total_invoices"])],
        ["Total Items Sold", format_number(stats["total_items_sold"])],
        ["Total Revenue", format_currency(stats["total_revenue"])],
        ["Total Cost", format_currency(stats["total_cost"])],
        ["Total Profit", format_currency(stats["total_profit"])],
        ["Profit Margin", f"{stats['profit_margin']:.2f}%"]
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 3*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    
    story.append(stats_table)
    story.append(Spacer(1, 20))
    
    # Top & Bottom Products
    if summary["top_product"]:
        story.append(Paragraph("Best & Worst Performers", heading_style))
        
        top = summary["top_product"]
        bottom = summary["bottom_product"]
        
        performers_data = [
            ["Rank", "Product Name", "Units Sold", "Revenue", "Profit"],
            ["🥇 Top", top[1], format_number(top[2]), format_currency(top[3]), format_currency(top[4])],
        ]
        
        if bottom:
            performers_data.append(
                ["📉 Lowest", bottom[1], format_number(bottom[2]), format_currency(bottom[3]), format_currency(bottom[4])]
            )
        
        performers_table = Table(performers_data, colWidths=[1*inch, 2*inch, 1.2*inch, 1.4*inch, 1.4*inch])
        performers_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f093fb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightblue, colors.lightpink])
        ]))
        
        story.append(performers_table)
        story.append(Spacer(1, 20))
    
    # Top Products Details
    if top_products:
        story.append(Paragraph("Top 10 Products by Sales Volume", heading_style))
        
        products_data = [["#", "Product Name", "Qty Sold", "Revenue", "Profit", "Margin %"]]
        
        for idx, product in enumerate(top_products, 1):
            product_id, name, sku, qty, revenue, avg_price, cost, profit, num_sales = product
            margin = (profit / revenue * 100) if revenue > 0 else 0
            products_data.append([
                str(idx),
                name[:25] + "..." if len(name) > 25 else name,
                format_number(qty),
                format_currency(revenue),
                format_currency(profit),
                f"{margin:.1f}%"
            ])
        
        products_table = Table(products_data, colWidths=[0.4*inch, 2.2*inch, 0.9*inch, 1.3*inch, 1.3*inch, 0.9*inch])
        products_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4ECDC4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ]))
        
        story.append(products_table)
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


def render_sales_analysis():
    """Main function to render sales analysis page"""
    st.title("📊 Sales Performance Analysis")
    st.markdown("---")
    
    # Get comprehensive summary
    summary = get_sales_analysis_summary()
    
    # Overall Statistics Cards
    st.markdown("### 📈 Overall Performance Metrics")
    stats = summary["overall_stats"]
    
    metrics = [
        {"label": "Total Invoices", "value": format_number(stats["total_invoices"])},
        {"label": "Items Sold", "value": format_number(stats["total_items_sold"])},
        {"label": "Total Revenue", "value": format_currency(stats["total_revenue"])},
        {"label": "Total Cost", "value": format_currency(stats["total_cost"])},
        {"label": "Total Profit", "value": format_currency(stats["total_profit"])},
        {"label": "Profit Margin", "value": f"{stats['profit_margin']:.2f}%"},
    ]
    
    render_metric_cards(metrics, columns=3)
    
    st.markdown("---")
    
    # Top and Bottom Products
    render_top_bottom_products(summary)
    
    st.markdown("---")
    
    # Charts Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Top products bar chart
        render_top_products_chart(summary["top_products_for_chart"])
    
    with col2:
        # Profit margin chart
        profit_margins = get_profit_margin_by_product(limit=6)
        render_profit_margin_chart(profit_margins)
    
    st.markdown("---")
    
    # Additional Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Category performance
        categories = get_category_sales_performance()
        render_category_performance(categories)
    
    with col2:
        # Sales trend
        render_sales_trend(months=6)
    
    st.markdown("---")
    
    # Top Customers
    st.markdown("### 👥 Top Customers by Purchase Amount")
    customers = get_customer_sales_ranking(limit=10)
    
    if customers:
        df_customers = pd.DataFrame(customers, columns=[
            "ID", "Customer Name", "Total Invoices", "Total Purchase", "Total Paid", "Total Due"
        ])
        
        # Format currency columns
        for col in ["Total Purchase", "Total Paid", "Total Due"]:
            df_customers[col] = df_customers[col].apply(format_currency)
        
        st.dataframe(df_customers, use_container_width=True, hide_index=True)
    else:
        st.info("No customer purchase data available")
    
    st.markdown("---")
    
    # Export Section
    st.markdown("### 📄 Export Report")
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("📥 Download PDF Report", use_container_width=True):
            try:
                pdf_buffer = export_to_pdf()
                st.download_button(
                    label="📄 Click to Download PDF",
                    data=pdf_buffer,
                    file_name=f"Sales_Analysis_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                st.success("PDF generated successfully!")
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")
    
    with col2:
        # Export detailed data as CSV
        if st.button("📊 Download CSV Data", use_container_width=True):
            products = get_product_sales_summary(limit=100)
            if products:
                df = pd.DataFrame(products, columns=[
                    "Product ID", "Product Name", "SKU", "Quantity Sold",
                    "Total Revenue", "Avg Selling Price", "Total Cost", "Total Profit", "Number of Sales"
                ])
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Click to Download CSV",
                    data=csv,
                    file_name=f"Product_Sales_Data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                st.success("CSV data ready for download!")
            else:
                st.warning("No data available to export")
