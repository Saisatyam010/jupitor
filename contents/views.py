import openai
from rest_framework import viewsets
from .models import Content
from .serializers import ContentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from titles.models import Title
from products.models import Product

openai.api_key = settings.OPENAI_API_KEY


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    @action(detail=False, methods=['post'])
    def generate_content(self, request):
        titles = request.data.get('titles', [])
        product_id = request.data.get('product_id')
        objective_length = request.data.get('objective_length', 0)
        procedure_length = request.data.get('procedure_length', 0)
        explanation_length = request.data.get('explanation_length', 0)
        home_ingredients_count = request.data.get('home_ingredients_count', 0)
        box_ingredients_count = request.data.get('box_ingredients_count', 0)
        custom_prompt = request.data.get('custom_prompt', '')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product does not exist'}, status=404)

        generated_contents = []
        for title_id in titles:
            try:
                title = Title.objects.get(id=title_id)
            except Title.DoesNotExist:
                return Response({'error': f'Title with id {title_id} does not exist'}, status=404)

            prompt_details = f"Generate content for the experiment '{title.title_name}' with the following details:"
            prompt_details += f"\n- Objective (max length: {objective_length} characters) followed by '#end#',"
            prompt_details += f"\n- Procedure (max length: {procedure_length} characters) followed by '#end#',"
            prompt_details += f"\n- Explanation (max length: {explanation_length} characters) followed by '#end#',"
            prompt_details += f"\n- Home Ingredients (count: {home_ingredients_count}) followed by '#end#',"
            prompt_details += f"\n- Box Ingredients (count: {box_ingredients_count})"

            if custom_prompt:
                prompt_details += f"\n- Custom prompt: {custom_prompt} followed by '#end#'"

            messages = [
                {"role": "system", "content": f"You are a model GPT-3.5-turbo and you were asked to: {prompt_details}"},
                {"role": "user", "content": f"Please write the details in the required format."},
            ]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                n=1,  # Generate only one result
                max_tokens=objective_length + procedure_length + explanation_length + home_ingredients_count * 10 + box_ingredients_count * 10
            )

            generated_text = response['choices'][0]['message']['content'].strip().split('#end#')

            content_parts = {
                'objective': generated_text[0].strip() if len(generated_text) > 0 else '',
                'procedure': generated_text[1].strip() if len(generated_text) > 1 else '',
                'explanation': generated_text[2].strip() if len(generated_text) > 2 else '',
                'home_ingredients': generated_text[3].strip() if len(generated_text) > 3 else '',
                'box_ingredients': generated_text[4].strip() if len(generated_text) > 4 else '',
                'custom_command': custom_prompt
            }

            new_content = Content(
                title=title,
                product=product,
                objective=content_parts['objective'],
                procedure=content_parts['procedure'],
                explanation=content_parts['explanation'],
                home_ingredients=content_parts['home_ingredients'],
                box_ingredients=content_parts['box_ingredients'],
                custom_command=content_parts['custom_command'],
            )

            new_content.save()

            generated_contents.append(content_parts)

        return Response(generated_contents)
