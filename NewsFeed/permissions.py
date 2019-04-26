from rest_framework import permissions


class IsSchoolOwner(permissions.BasePermission):
    """
    학교는 생성한 사람만 정보를 수정/삭제 할 수 있다.
    """
    
    def has_object_permission(self, request, view, obj):
        # 조회는 모두 가능
        if request.method in permissions.SAFE_METHODS:
            return True
        # 수정/삭제의 경우 소유자만 가능
        return obj.owner == request.user
