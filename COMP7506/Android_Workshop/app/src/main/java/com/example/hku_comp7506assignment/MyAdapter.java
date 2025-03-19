package com.example.hku_comp7506assignment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import java.util.List;
import java.util.Map;

public class MyAdapter extends RecyclerView.Adapter<MyAdapter.ViewHolder> {

    private List<Map<String, String>> dataList;

    public MyAdapter(List<Map<String, String>> dataList) {
        this.dataList = dataList;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.course_list_item, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        Map<String, String> data = dataList.get(position);
        holder.courseNameTextView.setText(data.get("CourseName"));
        holder.teachersTextView.setText(data.get("Teachers"));
    }

    @Override
    public int getItemCount() {
        return dataList.size();
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {
        TextView courseNameTextView;
        TextView teachersTextView;

        public ViewHolder(View itemView) {
            super(itemView);
            courseNameTextView = itemView.findViewById(R.id.coursename);
            teachersTextView = itemView.findViewById(R.id.teachers);
        }
    }
}