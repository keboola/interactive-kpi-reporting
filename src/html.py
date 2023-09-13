html_code = '''
    <div style="display: flex; justify-content: left; margin:5% 0">
        <div style="width: 50%;text-align:left">
            <strong>Key Performance Indicators Description:</strong>
            <p></p>
            <p>Turnover: Total turnover of paid orders in selected period.</p>
            <p>Orders: Count of orders in selected period.</p>
            <p>Average Order Value: Average amount spent by customers per transaction in selected period.</p>
            <p>Total Customer: Total number of customers in selected period.</p>
            <p>New Customers: Number of customers with the first order in selected period.</p>
        </div>
    </div>
    '''

css_style = """
<style>
    .subheader {
        font-size: 24px;
        font-weight: bold;
        margin-top: 50px;
        margin-bottom:50px
    }
</style>
"""
title= {
    "filters":'<p class="subheader">Time Period</p>',
    "statistics":'<p class="subheader">Key Performance Indicators</p>',
}
