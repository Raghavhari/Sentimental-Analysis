from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import subprocess
from . import python_script

# Create your views here.
# request -> response
# request handler
# action

def get_input(request):
    # pull data from db
    # transform
    # send email
    #return HttpResponse('hello')
    return render(request,'ui.html')

def analyze_sentiment(request):
    if request.method == 'GET':
        # Retrieve form data from the request
        hashtag = request.GET.get('hashtag')
        fdate = request.GET.get('fdate')
        
        # Now you can process the form data (e.g., perform sentiment analysis)
        # Add your code here to perform sentiment analysis using the hashtag and filter date
        
        # For now, just return a simple HTTP response with the form data
    #return HttpResponse(f"Hashtag: {hashtag}, Filter Date: {fdate}")
        try:
            # Replace 'python_script.py' with the name of your Python file
            #result = subprocess.run(['python', 'python_script.py', hashtag, fdate], capture_output=True, text=True)
            # Call your sentiment analysis function with hashtag and date
            # Assuming sentiment_analysis_module has a function named analyze_sentiment
            sentiment_result = python_script.main(hashtag, fdate)
            # Capture the output of the Python script
            #output = result.stdout
            
            # Render the result in an HTML template
            #template = loader.get_template('sentiment_results.html')
            #context = {'output': output}
            #return HttpResponse(template.render(context, request))
            # Render the result in another template
            return render(request, 'result.html', {'sentiment_result': sentiment_result})
        except Exception as e:
            #return HttpResponse("Invalid request method")
            return HttpResponse(f"An error occurred: {str(e)}") 
        '''try:
            # Replace 'python_script.py' with the name of your Python file
            result = subprocess.run(['python', 'python_script.py', hashtag, fdate], capture_output=True, text=True)
            # Capture the output of the Python script
            output = result.stdout
            
            # Render the result in an HTML template
            template = loader.get_template('sentiment_results.html')
            context = {'output': output}
            rendered_html = template.render(context)
            
            # Return the rendered HTML directly
            return HttpResponse(rendered_html)
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}")'''
        '''try:
            # Run the Python script with the provided hashtag and fdate
            subprocess.run(['python', 'python_script.py', hashtag, fdate])
            # Return a success message or redirect to another page
            return HttpResponse("Sentiment analysis completed successfully.")
        except Exception as e:
            # Return an error message
            return HttpResponse(f"An error occurred: {str(e)}")'''