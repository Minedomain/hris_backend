from rest_framework import viewsets, generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from .serializers import *

class SurveyViewset(viewsets.ModelViewSet):
    queryset = Survey.objects.all().order_by('id')
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "survey_id"
    lookup_value_regex = "[^/]+"

# Question
class SurveyQuestionViewset(viewsets.ModelViewSet):
    queryset = SurveyQuestion.objects.all().order_by('id')
    serializer_class = SurveyQuestionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "question_id"
    lookup_value_regex = "[^/]+"

    action_serializers = {
        'create': SurveyQuestionSerializer,
        'retrieve': SurveyQuestionRetrieveSerializer,
        'list': SurveyQuestionSerializer,
        'update': SurveyQuestionRetrieveSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(SurveyQuestionViewset, self).get_serializer_class()

    def get_queryset(self):
        if hasattr(self, 'action'):
            return SurveyQuestion.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'success': 'Survey Question has been deleted successfully'}, status=status.HTTP_200_OK)

class SurveyQuestionRetrieveView(generics.ListAPIView):
    serializer_class = SurveyQuestionRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try: 
            request = self.request
            survey_id = request.GET.get('survey_id')
            return SurveyQuestion.objects.filter(survey_id__survey_id= survey_id)
        except:
            return None
    
    def get(self, request):
        data = SurveyQuestionRetrieveSerializer(self.get_queryset(),many=True).data
        if data == []:
            return Response({'error': "Survey question/s not found."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status.HTTP_200_OK)

# Option
class SurveyOptionViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = SurveyOption.objects.all().order_by('id')
    serializer_class = SurveyOptionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "option_id"
    lookup_value_regex = "[^/]+"

    action_serializers = {
        'create': SurveyOptionSerializer,
        'retrieve': SurveyOptionRetrieveSerializer,
        'list': SurveyOptionSerializer,
        'update': SurveyOptionRetrieveSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(SurveyOptionViewset, self).get_serializer_class()

    def get_queryset(self):
        if hasattr(self, 'action'):
            return SurveyOption.objects.all()

class SurveyOptionRetrieveView(generics.ListAPIView):
    serializer_class = SurveyOptionRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try: 
            request = self.request
            question_id = request.GET.get('question_id')
            return SurveyOption.objects.filter(question_id__question_id= question_id)
        except:
            return None
    
    def get(self, request):
        data = SurveyOptionRetrieveSerializer(self.get_queryset(),many=True).data
        if data == []:
            return Response({'error': "Survey option/s not found."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status.HTTP_200_OK)

# Answer
class SurveyAnswerViewset(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = SurveyAnswer.objects.all().order_by('id')
    serializer_class = SurveyAnswerSerializer
    permission_classes = [IsAuthenticated]

class SurveyAnswerRetrieveView(generics.ListAPIView):
    serializer_class = SurveyAnswerRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try: 
            request = self.request
            question_id = request.GET.get('question_id')
            employee_id = request.GET.get('employee_id')
            if question_id:
                filterRetrieve = SurveyAnswer.objects.filter(question_id__question_id = question_id)
            elif employee_id:
                filterRetrieve = SurveyAnswer.objects.filter(employee_id__employee_id = employee_id)
            return filterRetrieve
        except:
            return None
    
    def get(self, request):
        data = SurveyAnswerRetrieveSerializer(self.get_queryset(),many=True).data
        if data == []:
            return Response({'error': "Survey answer/s not found."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status.HTTP_200_OK)

# Response
class SurveyResponseViewset(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = SurveyResponse.objects.all().order_by('id')
    serializer_class = SurveyResponseSerializer
    permission_classes = [IsAuthenticated]

class SurveyResponseRetrieveView(generics.ListAPIView):
    serializer_class = SurveyResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try: 
            request = self.request
            survey_id = request.GET.get('survey_id')
            employee_id = request.GET.get('employee_id')
            if survey_id:
                filterRetrieve = SurveyResponse.objects.filter(survey_id__survey_id = survey_id)
            elif employee_id:
                filterRetrieve = SurveyResponse.objects.filter(employee_id__employee_id = employee_id)
            return filterRetrieve
        except:
            return None
    
    def get(self, request):
        data = SurveyResponseSerializer(self.get_queryset(),many=True).data
        if data == []:
            return Response({'error': "Survey response/s not found."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status.HTTP_200_OK)
