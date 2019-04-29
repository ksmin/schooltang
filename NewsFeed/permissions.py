from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    학교는 생성한 사람만 정보를 수정/삭제 할 수 있다.
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # 조회는 모두 가능
        if request.method in permissions.SAFE_METHODS:
            return True
        # 수정/삭제의 경우 소유자만 가능
        return obj.owner == request.user


class IsSelf(permissions.BasePermission):
    """
    프로파일 API에 적용되는 권한으로 사용자 스스로의 오브젝트에만 접근 할 수 있다.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
        
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated() and obj == request.user
