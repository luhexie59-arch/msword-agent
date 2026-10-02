#define _CRT_SECURE_NO_WARNINGS
#include <windows.h>
#include <stdio.h>

DWORD strToNum(char s[]) {
    DWORD result = 0;
    while (*s) {
        result = result * 10 + (*s - '0');
        s++;
    }
    return result;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        return -1;
    }
    DWORD N = strToNum(argv[2]);

    CHAR    lpPath[MAX_PATH * 2];
    CHAR    WnDr[MAX_PATH];
    CHAR    WINWORDPATH[MAX_PATH] = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE";

    SIZE_T                      sThreadAttList = NULL;
    PPROC_THREAD_ATTRIBUTE_LIST pThreadAttList = NULL;

    STARTUPINFOEXA      SiEx = { 0 };
    PROCESS_INFORMATION Pi = { 0 };

    DWORD   targetPid = strToNum(argv[N + 3]);  // ppid is the first argument
    HANDLE  hParent = NULL;

    RtlSecureZeroMemory(&SiEx, sizeof(STARTUPINFOEXA));
    RtlSecureZeroMemory(&Pi, sizeof(PROCESS_INFORMATION));
    SiEx.StartupInfo.cb = sizeof(STARTUPINFOEXA);

    hParent = OpenProcess(PROCESS_ALL_ACCESS, FALSE, targetPid);
    if (hParent == NULL) {
        printf("[!] OpenProcess failed: %d\n", GetLastError());
        return -1;
    }

    if (!GetEnvironmentVariableA("WINDIR", WnDr, MAX_PATH)) {
        printf("[!] GetEnvironmentVariableA failed: %d\n", GetLastError());
        return -1;
    }

    sprintf(lpPath, "%s /n %s", WINWORDPATH, argv[N + 4]);

    InitializeProcThreadAttributeList(NULL, 1, NULL, &sThreadAttList);

    pThreadAttList = (PPROC_THREAD_ATTRIBUTE_LIST)HeapAlloc(
        GetProcessHeap(), HEAP_ZERO_MEMORY, sThreadAttList
    );
    if (pThreadAttList == NULL) {
        printf("[!] HeapAlloc failed: %d\n", GetLastError());
        return -1;
    }

    if (!InitializeProcThreadAttributeList(pThreadAttList, 1, NULL, &sThreadAttList)) {
        printf("[!] InitializeProcThreadAttributeList failed: %d\n", GetLastError());
        return -1;
    }

    if (!UpdateProcThreadAttribute(
        pThreadAttList, NULL,
        PROC_THREAD_ATTRIBUTE_PARENT_PROCESS,
        &hParent, sizeof(HANDLE),
        NULL, NULL)) {
        printf("[!] UpdateProcThreadAttribute failed: %d\n", GetLastError());
        return -1;
    }

    SiEx.lpAttributeList = pThreadAttList;

    if (!CreateProcessA(
        NULL, lpPath,
        NULL, NULL, FALSE,
        EXTENDED_STARTUPINFO_PRESENT,
        NULL, NULL,
        &SiEx.StartupInfo, &Pi)) {
        printf("[!] CreateProcessA failed: %d\n", GetLastError());
        return -1;
    }

    DeleteProcThreadAttributeList(pThreadAttList);
    CloseHandle(hParent);
    CloseHandle(Pi.hProcess);
    CloseHandle(Pi.hThread);

    return 0;
}