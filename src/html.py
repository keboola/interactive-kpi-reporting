html_code = '''
    <div style="display: flex; justify-content: center; margin:5% 0">
        <div style="width: 50%;text-align:left">
            <strong>Filters:</strong>
            <p></p>
            <p>Gender: Passenger's gender (male, female).</p>
            <p>Age: Passengers' age on the Titanic.</p>
            <p>Survived: Indicates passenger survival status.</p>
        </div>
        <div style="width: 50%;text-align:left">
            <strong>Metrics:</strong>
            <p></p>
            <p>Total: The total number of people or categorized by gender.</p>
            <p>Average Age: The average age of all passengers or categorized by gender.</p>
            <p>Total Survived: The total number of survivors among all passengers or categorized by gender.</p>
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
    "filters":'<p class="subheader">Filters</p>',
    "statistics":'<p class="subheader">Statistics</p>',
}
