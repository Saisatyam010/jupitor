from rest_framework import viewsets, filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Prompt
from .serializers import PromptSerializer
from .bulk_operations import bulk_delete_prompts, bulk_update_prompts
from .search import PromptSearchFilter
from .filters import PromptFilter
import requests
from django.conf import settings
import logging
from titles.models import Title

# Initialize logger
logger = logging.getLogger(__name__)

class PromptViewSet(viewsets.ModelViewSet):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter, PromptSearchFilter]
    filterset_class = PromptFilter
    search_fields = ['prompt_text', 'id', 'product__id']
    ordering_fields = ['serial_number', 'id', 'created_at', 'modified_at', 'product_id']

    @action(detail=False, methods=['post'])
    def generate_titles(self, request):
        product_id = request.data.get('product_id')
        no_of_characters = request.data.get('no_of_characters')
        prompt_text = request.data.get('prompt')

        if not all([product_id, no_of_characters, prompt_text]):
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if API key is being loaded correctly
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            return Response({'error': 'OpenAI API key is not set.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.info(f"Using OpenAI API Key: {api_key}")

        # Adjust max_tokens to a higher value to accommodate the response
        max_tokens = 1000  # Adjust this value based on your requirements

        # Call ChatGPT API to generate titles using GPT-4
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_text}
            ],
            "max_tokens": max_tokens
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

        if response.status_code != 200:
            logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
            return Response({'error': 'Error communicating with OpenAI API', 'details': response.text}, status=response.status_code)

        response_data = response.json()
        generated_titles = []
        for choice in response_data['choices']:
            titles = choice['message']['content'].strip().split("\n")
            generated_titles.extend(titles)

        # Clean the titles
        cleaned_titles = [title.lstrip("0123456789. \"").rstrip("\"") for title in generated_titles]

        # Store the generated titles and prompt text in the session for temporary storage
        request.session['generated_titles'] = cleaned_titles
        request.session['prompt_text'] = prompt_text
        request.session['product_id'] = product_id

        return Response({'generated_titles': cleaned_titles}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='save_prompt')
    def save_prompt(self, request):
        product_id = request.session.get('product_id')
        generated_titles = request.session.get('generated_titles', [])
        prompt_text = request.session.get('prompt_text', '')

        if not product_id or not generated_titles:
            return Response({'error': 'No titles to save or prompt not found.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create or update Prompt object
            prompt, created = Prompt.objects.get_or_create(product_id=product_id, prompt_text=prompt_text)
            prompt.times_generated += 1
            prompt.save()

            # Store titles in the Title model and update title_name in Prompt
            title_objects = []
            for title_name in generated_titles:
                title_obj = Title.objects.create(
                    title_name=title_name,
                    prompt=prompt,
                    product_id=product_id
                )
                title_objects.append(title_obj)

            # Update the number of titles and title_name in Prompt
            prompt.no_of_titles = Title.objects.filter(prompt=prompt).count()
            prompt.title_name = "; ".join([title.title_name for title in Title.objects.filter(prompt=prompt)])
            prompt.save()

            # Clear the session data
            del request.session['generated_titles']
            del request.session['prompt_text']
            del request.session['product_id']

            return Response({'status': 'Prompt saved successfully.'}, status=status.HTTP_200_OK)
        except Prompt.DoesNotExist:
            return Response({'error': 'Prompt not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['put'], url_path='update_prompt')
    def update_prompt(self, request, pk=None):
        try:
            prompt = self.get_object()
            data = request.data

            # Update title_name and other fields if provided
            if 'title_name' in data:
                prompt.title_name = data['title_name']
                # Update title_name in related titles
                titles = Title.objects.filter(prompt=prompt)
                for title in titles:
                    title.title_name = data['title_name']
                    title.save()

            if 'titles' in data:
                prompt.no_of_titles = len(data['titles'])

            prompt.save()

            serializer = self.get_serializer(prompt)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Prompt.DoesNotExist:
            return Response({'error': 'Prompt not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], url_path='bulk_delete')
    def bulk_delete(self, request):
        return bulk_delete_prompts(request)

    @action(detail=False, methods=['post'], url_path='bulk_update')
    def bulk_update(self, request):
        return bulk_update_prompts(request)
